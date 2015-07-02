#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '3/18/15'

from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['shark-release']

c_DC = db['DC']
c_category = db['category']

condition = {
    'value': {
        '$gt': 1
    }
}

for dc in c_DC.find(condition):
    _id = dc['_id']
    shop_id = ObjectId(_id.split('-', 1)[0])
    category_name = _id.split('-', 1)[1]
    print shop_id, category_name,
    n = c_category.find(
        {
            'shop_id': shop_id,
            'name': category_name
        }
    ).count()
    print n