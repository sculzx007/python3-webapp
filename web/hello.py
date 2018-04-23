#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#作为网页
__author__ = 'lzx'

def application(environ, start_respone):
    start_respone('200 OK', [('Context-Type', 'text/html')])
    body = '<h1>hello %s</h1>'  % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]