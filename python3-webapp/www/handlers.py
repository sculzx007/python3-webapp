#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lzx'

' url handlers '

import re, time, json, logging, hashlib, base64,asyncio,_asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id
from apis import Page

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        raise('Error: %s' % e)
    if p < 0:
        p = 1
    return p

@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id = '1', name = 'Test Blog', summary = summary, created_at = time.time()-120),
        Blog(id = '2', name = 'Something New', summary = summary, created_at = time.time()-3600),
        Blog(id = '3', name = 'Learn Swift', summary = summary, created_at = time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
@get('/api/users')
def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())

    users = yield from User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
        return dict(page=p, users=users)