#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from itertools import groupby as gb
for key, group in gb('AAAABBBBCCCCDDDD'):
    print(key, list(group))
