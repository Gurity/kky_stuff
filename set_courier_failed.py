#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '3/17/15'

from pymongo import MongoClient
import datetime
import xlrd
from bson import ObjectId

book = xlrd.open_workbook(file_contents=file(u"/home/zh/Downloads/速递员注册有问题的.xls").read())
courier_ids = []
for sheet_num in range(0, book.nsheets):
    sh = book.sheet_by_index(sheet_num)
    for rx in range(2, sh.nrows):
        row = sh.row(rx)
        try:
            cid = row[1].value
            courier_ids.append(ObjectId(cid))
        except:
            print cid
            continue


client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['wukong-release']
c_courier = db['courier']
for cid in courier_ids:
    result = c_courier.update(
        { '_id': cid },
        { '$set': { 'status': 'failed' } }
    )
    print result
