#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lzx'

'''
default configurations
作为开发环境的标准配置
'''

configs = {
    'db':{
        'host':'127.0.0.1',
        'port':3306,
        'user':'www-data',
        'password':'www-data',
        'database':'awesome'
    },
    'session':{
        'secret':'Awesome'
    }
}
