# -*- coding: utf-8 -*-

import time
from feedparser import feedparser
from DateTime.DateTime import DateTime
from DateTime.interfaces import DateTimeError


# Accept these bozo_exceptions encountered by feedparser when parsing
# the feed:
ACCEPTED_FEEDPARSER_EXCEPTIONS = (feedparser.CharacterEncodingOverride, )

# store the feeds here (which means in RAM)
FEED_DATA = {}  # url: ({date, title, url, itemlist})

class RSSFeed(object):
    """an RSS feed"""

    # TODO: discuss whether we want an increasing update time here, probably not though
    FAILURE_DELAY = 10  # time in minutes after which we retry to load it after a failure

    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout

        self._items = []
        self._title = ""
        self._siteurl = ""
        self._loaded = False    # is the feed loaded
        self._failed = False    # does it fail at the last update?
        self._last_update_time_in_minutes = 0 # when was the feed last updated?
        self._last_update_time = None            # time as DateTime or Nonw

    @property
    def last_update_time_in_minutes(self):
        """return the time the last update was done in minutes"""
        return self._last_update_time_in_minutes

    @property
    def last_update_time(self):
        """return the time the last update was done in minutes"""
        return self._last_update_time

    @property
    def update_failed(self):
        return self._failed

    @property
    def ok(self):
        return (not self._failed and self._loaded)

    @property
    def loaded(self):
        """return whether this feed is loaded or not"""
        return self._loaded

    @property
    def needs_update(self):
        """check if this feed needs updating"""
        now = time.time()/60
        return (self.last_update_time_in_minutes+self.timeout) < now

    def update(self):
        """update this feed"""
        now = time.time()/60    # time in minutes
        
        # check for failure and retry
        if self.update_failed:
            if (self.last_update_time_in_minutes+self.FAILURE_DELAY) < now:
                return self._retrieveFeed()
            else:
                return False

        # check for regular update
        if self.needs_update:
            return self._retrieveFeed()

        return self.ok

    def _retrieveFeed(self):
        """do the actual work and try to retrieve the feed"""
        url = self.url
        if url!='':
            self._last_update_time_in_minutes = time.time()/60
            self._last_update_time = DateTime()
            d = feedparser.parse(url)
            if getattr(d, 'bozo', 0) == 1 and not isinstance(d.get('bozo_exception'),
                                              ACCEPTED_FEEDPARSER_EXCEPTIONS):
                self._loaded = True # we tried at least but have a failed load
                self._failed = True
                return False
            self._title = d.feed.title
            self._siteurl = d.feed.link
            self._items = []
            for item in d['items']:
                try:
                    link = item.links[0]['href']
                    itemdict = {
                        'title': item.title,
                        'url': link,
                        'summary': item.get('description', ''),
                    }
                    if hasattr(item, "updated"):
                        try:
                            itemdict['updated'] = DateTime(item.updated)
                        except DateTimeError:
                            # It's okay to drop it because in the
                            # template, this is checked with
                            # ``exists:``
                            pass
                except AttributeError:
                    continue
                self._items.append(itemdict)
            self._loaded = True
            self._failed = False
            return True
        self._loaded = True
        self._failed = True # no url set means failed
        return False # no url set, although that actually should not really happen

    @property
    def items(self):
        return self._items

    # convenience methods for displaying
    #

    @property
    def feed_link(self):
        """return rss url of feed for portlet"""
        return self.url.replace("http://", "feed://")

    @property
    def title(self):
        """return title of feed for portlet"""
        return self._title

    @property
    def siteurl(self):
        """return the link to the site the RSS feed points to"""
        return self._siteurl
