# -*- coding: utf-8 -*-
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin, Jinja2
from werkzeug import cached_property

from RssFeed import RSSFeed
from config import SitesRss

from debug import dbg 
import random

def get_RSS(self, name):
    news= {}
    D = SitesRss.get('URLS')
    L = SitesRss.get('NAMES')
      
    timeout = 60
    url = D.get(name,'')
    
    itens = RSSFeed(url, timeout)
    itens.update()
    
    news['titulo'] = L.get(name)
    news['noticias'] = itens.items
    
    return news

def get_menu(self, menu):
    #dbg()
    
    return False


# Define a dictionary with global filters.
custom_filters = {
      'get_RSS': get_RSS,
      'get_menu':get_menu,
}

class HomeHandler(RequestHandler, Jinja2Mixin):
    @cached_property
    def jinja2(self):
        return Jinja2.factory(self.app, 'jinja2', filters=custom_filters)
    
    def listName(self, L=[]):
        D = SitesRss.get('URLS')
        name = random.choice(D.keys())
        while name in L:
           name = random.choice(D.keys())
        
        return name
    
    def get(self):
        L = []
        while len(L) < 3:
            L.append(self.listName(L))
       
        context = {'names':L}
        return self.render_response('home.html', **context)

class NoticiasHandler(RequestHandler, Jinja2Mixin):
    def get(self, name):
        
       news = get_RSS(self, name)
       return self.render_response('news.html', **news)
   
   