#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '5/15/15'

from pymongo import MongoClient
from bson import ObjectId
import datetime

client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')

db_shark = client['shark-release']
db_wukong = client['wukong-release']

c_order = db_shark['order']
c_subtask = db_wukong['subtask']

STARTTIME = datetime.datetime(2015, 5, 15, 19)
DEADLIME = datetime.datetime(2015, 5, 15, 22)

today_orders = c_order.find(
    {
        'created_time': {
            "$gt": int( (STARTTIME - datetime.datetime.fromtimestamp(0)).total_seconds() * 1000 ),
            "$lt": int( (DEADLIME - datetime.datetime.fromtimestamp(0)).total_seconds() * 1000 )
        },
        'express_id': {
            '$exists': True
        }
    }
)

order_count = today_orders.count()
print order_count

bad_orders = []
for o in today_orders:
    subtask_id = o.get('express_id')
    if subtask_id:
        subtask = c_subtask.find_one(
            {
                '_id': subtask_id
            }
        )
        if not subtask:
            bad_orders.append(str(o['_id']))

print len(bad_orders)
