#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '5/8/15'

from pymongo import MongoClient

client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')
db_shark_debug = client['shark-debug']
c_item_ttt = db_shark_debug['item_ttt']

result = c_item_ttt.insert(
    {
        'foo': 'bar'
    }
)
print result
