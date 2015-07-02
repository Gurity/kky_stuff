#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/3/15'

from pymongo import MongoClient
import pickle

client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')

db_shark = client['shark-release']
db_wukong = client['wukong-release']

c_order = db_shark['order']
c_shop = db_shark['shop']
c_school = db_wukong['schools']
c_withdraw = db_wukong['withdraw']
c_courier = db_wukong['courier']


def SetOrderRegion():
    order_condition = {
        'school': {
            '$exists': False
        }
    }

    bad_shops = []

    orders = c_order.find(order_condition)
    for order in orders:
        shop = c_shop.find_one({'_id': order['shop_id']})
        school_id = shop['school_district']
        school = c_school.find_one({'_id': school_id})
        if not school:
            bad_shops.append(shop)
            continue
        condition = {
            '_id': order['_id']
        }
        updater = {
            '$set': {
                'region': school['region'],
                'province': school['province'],
                'city': school['city'],
                'school': school['name']
            }
        }
        result = c_order.update(condition, updater)
        print result

    pickle.dump(bad_shops, open('bad_shops.obj', 'w'))


def SetWithdrawSchool():
    withdraws = c_withdraw.find({
        'school_id': { '$exists': 0 }
    })
    for w in withdraws:
        courier_id = w.get('courier_id')
        if not courier_id:
            print 'no_courier_id', w['_id']
            continue
        courier = c_courier.find_one({'_id':courier_id})
        if not courier:
            print 'no_courier', courier_id
            continue
        school_id = courier.get('district_id')
        if school_id:
            result = c_withdraw.update(
                { '_id': w['_id'] },
                { '$set': { 'school_id': school_id } }
            )
            print result
        else:
            print 'no school', school_id


if __name__ == '__main__':
    SetWithdrawSchool()
