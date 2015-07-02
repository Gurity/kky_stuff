#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '3/13/15'

from pymongo import MongoClient
import pickle

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['shark-release']

c_school = db['school']
c_shop = db['shop']

schools = {}
for s in c_school.find({}):
    schools[s['_id']] = s
dumpf = open('schools.obj', 'wb')
pickle.dump(schools, dumpf)

shops = {}
for s in c_shop.find({}):
    shops[s['_id']] = s
dumpf = open('shops.obj', 'wb')
pickle.dump(shops, dumpf)
