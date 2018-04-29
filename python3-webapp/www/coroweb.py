#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lzx'

import asyncio, os, inspect, logging, functools
from urllib import parse
from aiohttp import web
from apis import APIError

def get(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    '''
    Define decorator @post('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

# fn中不带默认值的强制关键字参数为函数的输出
def get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    '''
    	'params' here is an OrderedDict consisting info of parameters of fn,
    	i.e., OrderDict{'a': <Parameter "a">, ...} 
    	where a is one of parameters of fn.
    	'''
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            # when 'name' is KEYWORD_ONLY and 'name' has no default value
            # 即不带默认值的强制关键字参数为函数的输出
            args.append(name)
        return tuple(args)

# fn中强制关键字参数为函数的输出
def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            # when 'name' is KEYWORD_ONLY
            # 也就是强制关键字参数为函数的输出
            args.append(name)
        return tuple(args)

# 检查fn的参数中是否含有关键字参数
def has_named_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

#检查fn的参数中是否含有**kw
def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            # 'VAR_KEYWORD' actually is **kw
            # 也就是寻找关键字参数（dict）
            return True

#fn的参数中是否含有'request'参数，且为最后一个参数（不考虑*args和**kw在内）
def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('Request parameter must be the last named parameter in function: %s %s' % (fn.__name__, str(sig)))
    return found
    # this is used to find whether 'request' is a parameter of fn.
    # VAR_POSITIONAL: *args, which depends on position to make input
    # KEYWORD_ONLY: must use keyword to make input rather than position
    # VAR_KEYWORD: **kw, which depends on keyword to make input
    # once 'request' is found, no other parameter except from '*args' and '**kw' is allowed to locate.


class RequestHandler(object):
    '''
    1.用于从URL函数中分析需要接收的参数；（Analyze the parameters of fn(request handler function)）
    2.从request中获取必须的参数，调用URL函数；（Retrieve info or kw from request）
    3.将结果转换为web.Response对象。（Call fn with input kw and get output as 'web.Request'）
    '''
    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)

    async def __call__(self, request):
        kw = None      #获取参数
        '''
         if fn has parameters like **kw or KEYWORD_ONLY(with or without default value)
         '''
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')

                ct = request.content_type.lower()
                if ct.startwith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object')
                    kw = params

                if ct.startwith('application/x-www-form-urlencoded') or ct.startwith('multipart/form-data'):
                   params = await request.post()
                   kw = dict(**params)
                else:
                    return  web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)

            if request.method == 'POST':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]



