#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/8/15'

from pymongo import MongoClient
import pickle
import Util


client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')

db_shark = client['shark-release']
db_wukong = client['wukong-release']
db_console = client['console-release']

c_order = db_shark['order']
c_shop = db_shark['shop']
c_school = db_wukong['schools']
c_console_user = db_console['users']

def SetOrderSchoolId():
    bad_orders = []
    condition = {
        'school_id': { '$exists': 0 }
    }
    orders = c_order.find(condition)
    for order in orders:
        shop_id = order['shop_id']
        shop = c_shop.find_one({'_id':shop_id})
        if shop:
            result = c_order.update(
                { '_id': order['_id'] },
                {
                    '$set': {
                        'school_id': shop['school_district']
                    }
                }
            )
        else:
            school_name = order.get('school')
            if school_name:
                school = c_school.find_one({'name': school_name})
                if school:
                    result = c_order.update(
                        { '_id': order['_id'] },
                        {
                            '$set': {
                                'school_id': school['_id']
                            }
                        }
                    )
                else:
                    bad_orders.append(order)
            else:
                bad_orders.append(order)

    pickle.dump(bad_orders, open('orders_no_shop.obj', 'w'))


def CheckShopSchool():
    shop_without_school = []
    bad_shops = []
    shop_condition = {
        'status': {
            '$in': ['open']
        }
    }
    shops = c_shop.find(shop_condition)
    for shop in shops:
        school_id = shop['school_district']
        school = c_school.find_one({'_id': school_id})
        if not school:
            shop_without_school.append(shop)
            order_condition = {
                'shop_id': shop['_id']
            }
            order_count = c_order.find(order_condition).count()
            if order_count > 0:
                print shop['_id']
                bad_shops.append(shop)
                latest_order = c_order.find(order_condition).sort('created_time', -1).next()
                print Util.TimestampToText(latest_order['created_time'])
            else:
                print '0 order shop: ', shop['_id']

    pickle.dump(bad_shops, open('bad_shops.obj', 'w'))

def SetConsoleUserSchoolId():
    bad_users = []
    users = c_console_user.find({})
    for user in users:
        school_name = user.get('school_name')
        if school_name != u'全部校区':
            school = c_school.find_one({'name': school_name})
            if school:
                result = c_console_user.update(
                    { '_id': user['_id'] },
                    {
                        '$set': {
                            'school_id': school['_id']
                        }
                    }
                )
            else:
                bad_users.append(user)

    pickle.dump(bad_users, open('bad_user.obj', 'w'))

if __name__ == '__main__':
    # CheckShopSchool()
    # SetOrderSchoolId()
    SetConsoleUserSchoolId()
