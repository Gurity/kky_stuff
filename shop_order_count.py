# -*- coding: utf-8 -*-
__author__ = 'zh'

from pymongo import MongoClient
import datetime
import pickle
from xlwt import *


def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6

start_time = int(totimestamp(datetime.datetime(2014, 11, 1, 0, 0))) * 1000
end_time = int(totimestamp(datetime.datetime(2015, 2, 1, 0, 0))) * 1000

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['nfw-release']
c_order = db['order']
c_shop = db['shop']

mobile_school = pickle.load(open("courier_school.obj",'rb'))
shop_order_count_by_month = pickle.load(open("shop_order_count_by_month.obj",'rb'))

shop_mobile = {}
for shop in c_shop.find({}, {'mobile': 1}):
    shop_id = shop.get('_id', '')
    if not shop_id:
        continue
    mobile = shop.get('mobile', '')
    if not mobile:
        continue
    shop_mobile[shop_id] = mobile


school_order_count_by_month = {}
for month,shop_order_count in shop_order_count_by_month.items():
    school_order_count = {}
    for shop_id,count in shop_order_count.items():
        mobile = shop_mobile.get(shop_id, '')
        if not mobile:
            continue
        school = mobile_school.get(mobile, '')
        if not school:
            continue
        current_count = school_order_count.setdefault(school, 0)
        school_order_count[school] = current_count + count
    school_order_count_by_month[month] = school_order_count

w = Workbook()
title = (u'学校', u'单量')
for m, order_count in school_order_count_by_month.items():
    ws = w.add_sheet(str(m)+u'月份')
    ws.write(0, 0, u'学校')
    ws.write(0, 1, u'单量')
    row = 1
    for s,c in order_count.items():
        ws.write(row, 0, s)
        ws.write(row, 1, c)
        row += 1
w.save(u'学校单量按月份统计.xls')
