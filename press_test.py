#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/10/15'

from pymongo import MongoClient

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')

db_shark = client['shark-release']
db_wukong = client['wukong-release']

c_order = db_shark['order']
c_shop = db_shark['shop']
c_school = db_wukong['schools']


orders = list(c_order.find({}))

for o in orders:
    print o

