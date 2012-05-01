# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
         Rule('/', name='home', handler='views.handlers.HomeHandler'),
         Rule('/news/<string:name>', name='noticias', handler='views.handlers.NoticiasHandler'),
         
         Rule('/hello', name='hello-world', handler='hello_world.handlers.HelloWorldHandler'),
         Rule('/pretty', name='hello-world-pretty', handler='hello_world.handlers.PrettyHelloWorldHandler'),
]
