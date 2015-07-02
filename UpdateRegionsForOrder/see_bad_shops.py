#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/3/15'

import pickle

bad_shops = pickle.loads(open('bad_shops.obj', 'r').read())

ids = []

for bs in bad_shops:
    if not bs['_id'] in ids:
        ids.append(bs['_id'])
        print bs['_id'], bs['name']
