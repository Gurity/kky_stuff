#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '6/30/15'


from pymongo import MongoClient
from bson import ObjectId
import pickle
import datetime
import time
import sys
import logging
import tablib
import xlrd
import decimal


client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')

db_wukong = client['wukong-release']
db_console = client['console-release']

c_courier = db_wukong['courier']
c_log = db_console['log']
c_expense = db_wukong['expend']
c_withdraw = db_wukong['withdraw']

start_dt = datetime.datetime(2015, 6, 28)
end_dt = datetime.datetime(2015, 6, 30, 14)
start_timestamp = int(time.mktime(start_dt.timetuple()) * 1000)
end_timestamp = int(time.mktime(end_dt.timetuple()) * 1000)


'''
unfreeze_logs = list(c_log.find(
    {
        'action': 'courier_account',
        'arguments.freeze': 'unfreeze',
        'created_time': {
            '$gte': start_timestamp,
            '$lt': end_timestamp
        }
    }
))

unfreeze_courier_ids = [ ObjectId(log['arguments']['id'][0]) for log in unfreeze_logs]

headers = (
    '速递员ID',
    '速递员所属校区',
    '速递员姓名',
    '速递员手机号'
)
couriers = list(c_courier.find(
    {
        '_id': { '$in': unfreeze_courier_ids }
    }
))
lines = []
for c in couriers:
    line = (
        str(c['_id']),
        c.get('school', ''),
        c.get('name', ''),
        c.get('mobile', '')
    )
    lines.append(line)
data = tablib.Dataset(*lines, headers=headers)
with open('couriers.xls', 'wb') as f:
    f.write(data.xls)

bad_expense = list(c_expense.find(
    {
        'courier_id': { '$in': unfreeze_courier_ids },
        'status': { '$in': ['unprocessed', 'freezed'] }
    }
))
'''

bad_expense = list(c_expense.find(
    {
        'status': { '$in': ['freezed'] }
    }
))

bad_withdraw_ids = []
bad_expense_ids = []

for expense in bad_expense:
    fine_amount = expense['fine_amount']
    if fine_amount > 0:
        result = c_courier.update(
            { '_id': expense['courier_id'] },
            {
                '$inc': {
                    'debt': int(fine_amount)
                }
            }
        )
        print result

    bad_withdraw_ids.append(expense['withdraw_id'])
    bad_expense_ids.append(expense['_id'])

result = c_withdraw.update(
    { '_id': { '$in': bad_withdraw_ids} },
    {
        '$set': {
            'status': 'unprocessed',
            'unfreezed_time': int(time.time() * 1000)
        }
    },
    multi=True
)
print result

result = c_expense.remove(
    { '_id': { '$in': bad_expense_ids } }
)
print result
