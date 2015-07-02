#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '3/13/15'

from pymongo import MongoClient
import datetime
import pickle

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['nfw-release']

c_zone = db['zone']
c_column = db['column']
c_item = db['item']


zone_id_2_name = {} # { _id: city_name }
zone_name_2_id = {}

zone_condition = {
    'name': { '$exists': 1 }
}
for z in c_zone.find({}):
    name = z.get('name', None)
    id = z.get('_id', None)
    if name and id:
        zone_id_2_name[id] = name
        zone_name_2_id[name] = id

dumpf1 = open('zone_id_2_name.obj', 'wb')
pickle.dump(zone_id_2_name, dumpf1)
dumpf2 = open('zone_name_2_id.obj', 'wb')
pickle.dump(zone_name_2_id, dumpf2)

column_map = {} # { _id: {} }
for c in c_column.find({}):
    id = c.get('_id', None)
    name = c.get('name', None)
    priority = c.get('priority', 0)
    items = c.get('items', [])
    zone_id = c.get('zone_id', None)
    if not name or not zone_id:
        continue
    column_map[id] = {
        'name': name,
        'priority': priority,
        'items': items,
        'zone_id': zone_id
    }

dumpf3 = open('column_info.obj', 'wb')
pickle.dump(column_map, dumpf3)

item_info = {}
item_condition = {
    'status': 'on_sale',
    'name': { '$exists': 1 },
    'price': { '$exists': 1 }
}
for i in c_item.find(item_condition):
    item_info[i['_id']] = {
        'name': i.get('name', ''),
        'price': i.get('price', 0),
        'priority': i.get('priority', 0),
        'description': i.get('description', ''),
        'image_id': i.get('image_id', None)
    }

dumpf4 = open('item_info.obj', 'wb')
pickle.dump(item_info, dumpf4)