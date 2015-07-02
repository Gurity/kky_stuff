#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/27/15'

DB_HOST = ''

from pymongo import MongoClient
import pickle
import re
from bson import ObjectId

client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')

db_shark = client['shark-release']
db_wukong = client['wukong-release']

c_task = db_wukong['task']
c_subtask = db_wukong['subtask']
c_bill = db_wukong['bill']
c_withdraw = db_wukong['withdraw']
c_school = db_wukong['schools']
c_courier = db_wukong['courier']

COURIERS = [
    {
        'name': u'周西洋',
        'mobile': '18319539810',
        '_id': ObjectId("552d0deb778d17053aba1f28")
    },
    {
        'name': u'林俊辉',
        'mobile': '18344269752',
        '_id': ObjectId("552cc488778d17053ab93341")
    },
    {
        'name': u'李子轩',
        'mobile': '15702098091',
        '_id': ObjectId("55193566778d1704f442c6da")
    },
    {
        'name': u'朱鑫华',
        'mobile': '18318120023',
        '_id': ObjectId("552b9828778d1762c070c87e")
    },
    {
        'name': u'周多妍',
        'mobile': '15766382294',
        '_id': ObjectId("551577b0778d1705536a000b")
    },
    {
        'name': u'谭德强',
        'mobile': '15766271912',
        '_id': ObjectId("550a531c778d1704e2246cc6")
    },
    {
        'name': u'许立伟',
        'mobile': '13670401261',
        '_id': ObjectId("552a744c778d1745da9e820b")
    },
    {
        'name': u'陈一锦',
        'mobile': '15768863726',
        '_id': ObjectId("552924a9778d170533d657c5")
    },
    {
        'name': u'黄俊',
        'mobile': '15766382180',
        '_id': ObjectId("55292fec778d170533d67a82")
    }
]

couriers = list(c_courier.find(
    {
        '$or': [
            { 'name': { '$in': [c['name'] for c in COURIERS ] } },
            { 'mobile': { '$in': [c['mobile'] for c in COURIERS ] } }
        ]
    }
))

for c in COURIERS:
    print c.get('name'), c.get('mobile')

    bill_money = 0
    bills = c_bill.find(
        {
            'courier_id': c['_id']
        }
    )
    for b in bills:
        bill_money += b['money']

    withdraw_money = 0
    withdraws = c_withdraw.find(
        {
            'courier_id': c['_id']
        }
    )
    for w in withdraws:
        withdraw_money += w['money']

    c['bill_money'] = bill_money
    c['withdraw_money'] = withdraw_money

for c in couriers:
    print c.get('name'), c['mobile'],
    for C in COURIERS:
        if c.get('name') == C['name'] or c.get('mobile') == C['mobile']:
            balance = C.get('bill_money', 0) - C.get('withdraw_moeny', 0)
            print balance
            '''
            result = c_courier.update(
                { '_id': c['_id'] },
                {
                    '$set': {
                        'balance': int(balance)
                    }
                }
            )
            print result
            '''