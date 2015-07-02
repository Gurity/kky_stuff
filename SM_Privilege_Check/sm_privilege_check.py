#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/8/15'


from pymongo import MongoClient
import pickle

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')

db_console = client['console-release']

c_user = db_console['users']

broken_sm = []
users = c_user.find({})
for u in users:
    roles = u['roles']
    region = u['region']
    province = u['province']
    city = u['city']
    school = u['school_name']
    if 'sm' in roles:
        if region == u'全部大区' or province == u'全部省份' or city == u'全部城市' or school == u'全部校区':
            broken_sm.append(u)

for u in broken_sm:
    print u['_id']
