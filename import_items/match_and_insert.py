#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '3/13/15'

from pymongo import MongoClient
import pickle
import time
import datetime

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['shark-release']
c_category_temp = db['category_temp']
c_item_temp = db['item_temp']


zone_id_2_name = pickle.load(open("zone_id_2_name.obj",'rb'))
zone_name_2_id = pickle.load(open("zone_name_2_id.obj",'rb'))
schools = pickle.load(open("schools.obj",'rb'))
shops = pickle.load(open("shops.obj",'rb'))
columns = pickle.load(open("column_info.obj",'rb'))
items = pickle.load(open("item_info.obj",'rb'))

import xlrd
school_name_to_city_name = {}
book = xlrd.open_workbook(file_contents=file(u"school_data.xls").read())
for sheet_num in range(0, book.nsheets):
    sh = book.sheet_by_index(sheet_num)
    for rx in range(2, sh.nrows):
        row = sh.row(rx)
        school = row[0].value
        city = row[4].value
        school_name_to_city_name[school] = city

columns_of_zone_id = {}
for cid,c in columns.items():
    zone_id = c['zone_id']
    cols = columns_of_zone_id.setdefault(zone_id, [])
    cols.append(c)

for sid, shop in shops.items():
    district_id = shop.get('school_district', None)
    if not district_id:
        continue
    school = schools.get(district_id, None)
    if not school:
        continue

    city = school_name_to_city_name.get(school['school'], None)
    if not city:
        print school['school']
        continue

    zone_id = zone_name_2_id.get(city, None)
    if not zone_id:
        print city
        continue

    city_columns = columns_of_zone_id[zone_id]
    for column in city_columns:
        if column['name'] == u'跑腿':
            continue

        category_doc = {
            'shop_id': sid,
            'name': column['name'],
            'priority': column['priority'],
            'old': True
        }

        category_id = c_category_temp.insert(category_doc)
        print category_id

        item_dicts = column['items']
        for item_dict in item_dicts:
            item_id = item_dict['item_id']
            item = items.get(item_id, None)
            if not item:
                continue
            if not item.get('name', None):
                continue

            item_doc = {
                'category': category_id,
                'status': 'on_sale',
                'name': item['name'],
                'price': int(item['price']*100),
                'priority': item['priority'],
                'image_id': item['image_id'],
                'description': item['description'],
                'created_time': int(time.time()*1000),
                'shop_id': sid,
                'old': True
            }

            item_id = c_item_temp.insert(item_doc)
            print '    ' + str(item_id)


