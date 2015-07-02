#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '5/21/15'

from pymongo import MongoClient
from bson import ObjectId
import pickle
import datetime
import time
import sys
import logging

client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')

db_console = client['console-release']
db_shark = client['shark-release']
db_wukong = client['wukong-release']
c_order = db_shark['order']
c_school = db_wukong['schools']
c_order_statistics = db_console['order_statistics']


def create_order_statistics_of_date(date):
    start_date_str = date.strftime('%Y%m%d')
    start_time = int(time.mktime(date.timetuple()) * 1000)
    end_time = start_time + 24*60*60*1000

    print datetime.datetime.fromtimestamp(start_time/1000), datetime.datetime.fromtimestamp(end_time/1000)

    order_time_condition = {
        'created_time': {
            '$gte': start_time,
            '$lt': end_time
        }
    }

    school_orders = c_order.aggregate([
        { '$match': order_time_condition },
        {
            '$group': {
                '_id': '$school_id',
                'orders': {
                    '$push': {
                        'status': '$status',
                        'created_time': '$created_time'
                    }
                }
            }
        }
    ])['result']

    print len(school_orders)

    for so in school_orders:
        school_id = so['_id']
        orders = so['orders']
        order_statistic = {
            'date': start_date_str,
            'school_id': school_id,
            'unpaid': 0,
            'cancel': 0,
            'paid': 0,
            'sending': 0,
            'uncomment': 0,
            'done': 0,
            'refunded': 0,
            'item_price': 0,
            'delivery_price': 0,
            'discount_price': 0
        }
        for o in orders:
            order_statistic[o['status']] += 1
            order_statistic['item_price'] += o['items_price']
            order_statistic['delivery_price'] += o['delivery_price']
            order_statistic['discount_price'] += o['discount_price']

        school = c_school.find_one({'_id': school_id})
        if school:
            order_statistic['school_name'] = school['name']
            order_statistic['region'] = school['region']
            order_statistic['province'] = school['province']
            order_statistic['city'] = school['city']

        result = c_order_statistics.update(
            {
                'date': start_date_str,
                'school_id': school_id
            },
            {
                '$set': order_statistic
            },
            upsert=True
        )
        logging.info(result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        current_datetime = datetime.datetime.now()
        start_date = datetime.datetime(current_datetime.year, current_datetime.month, current_datetime.day)
        start_date -= datetime.timedelta(days=1)
    else:
        start_date = datetime.datetime.strptime(sys.argv[1], '%Y%m%d')

    for i in range(0, 1):
        create_order_statistics_of_date(start_date)
        start_date -= datetime.timedelta(days=1)
