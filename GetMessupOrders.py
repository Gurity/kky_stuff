#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/13/15'


from pymongo import MongoClient

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')

db_shark = client['shark-release']
db_wukong = client['wukong-release']

c_order = db_shark['order']
c_task = db_wukong['task']
c_subtask = db_wukong['subtask']

done_orders = c_order.find({
    'status': { '$in': ['done', 'uncomment'] }
})
messup_order = []
for order in done_orders:
    subtask_id = order['express_id']
    subtask = c_subtask.find_one({
        '_id': subtask_id,
        'status': { '$ne': 'done' }
    })
    if subtask and subtask['status'] != 'done':
        messup_order.append(order)
        print "'" + str(order['_id']) + "',"

print len(messup_order)
messup_order.sort(key=lambda o:o['created_time'])
print messup_order[0]