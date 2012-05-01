# -*- coding: utf-8 -*-
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin

from RssFeed import RSSFeed
from config import SitesRss

from debug import dbg 

class HomeHandler(RequestHandler, Jinja2Mixin):
    def get(self):
        context = {}
        return self.render_response('home.html', **context)

class NoticiasHandler(RequestHandler, Jinja2Mixin):
    def get(self, name):
        
        news= {}
        D = SitesRss.get('URLS')
        L = SitesRss.get('NAMES')
          
        timeout = 60
        url = D.get(name,'')

        itens = RSSFeed(url, timeout)
        itens.update()
        #dbg()
        
        news['titulo'] = L.get(name)
        news['noticias'] = itens.items

        return self.render_response('news.html', **news)
