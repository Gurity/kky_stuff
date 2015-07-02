#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '3/19/15'

from pymongo import MongoClient
from bson import ObjectId
import xlrd
import re

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['shark-release']

c_shop = db['shop']

exclude_schools = []
book = xlrd.open_workbook(file_contents=file(u"schools_to_exclude_new.xls").read())
for sheet_num in range(0, book.nsheets):
    sh = book.sheet_by_index(sheet_num)
    for rx in range(0, sh.nrows):
        row = sh.row(rx)
        school = row[0].value
        exclude_schools.append(school)

total = 0
for s in exclude_schools:
    REGEX = re.compile('.*' + s + '.*')
    condition = {
        'name': {
            '$regex': REGEX
        }
    }
    match_shops = c_shop.find(condition)
    for shop in match_shops:
        total += 1
        print s, shop['name'], shop['_id'],
        result = c_shop.update(
            { '_id': shop['_id'] },
            { '$set': { 'status': 'out' } }
        )
        print result

print total