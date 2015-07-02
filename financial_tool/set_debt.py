#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '6/17/15'

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
c_courier = db_wukong['courier']

my_input_stream = open('debt.xls', 'rb').read()
my_dataset = tablib.import_set(my_input_stream)

for debt_record in my_dataset:
    try:
        if debt_record[0] == '552d1fbc778d17053aba7057':
            courier_id = ObjectId(debt_record[0])
            debt_amount = int(decimal.Decimal(debt_record[5])*100)
            print debt_amount
    except:
        continue
