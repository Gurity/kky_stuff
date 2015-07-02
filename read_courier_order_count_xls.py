# -*- coding: utf-8 -*-
__author__ = 'zh'

import xlrd
import pickle
from xlwt import *


book = xlrd.open_workbook(file_contents=file(u"courier_order_count.xlsx").read())
mobile_order_count_by_month = {}
for sheet_num in range(0, book.nsheets):
    order_count = {}
    sh = book.sheet_by_index(sheet_num)
    current_school = None
    for rx in range(2, sh.nrows):
        row = sh.row(rx)
        mobile = row[1].value
        count = row[2].value
        if not mobile:
            continue
        try:
            mobile = str(int(mobile))
            count = int(count)
        except:
            continue
        order_count[mobile] = count
    mobile_order_count_by_month[sh.name] = order_count


mobile_2_school = pickle.load(open("courier_school.obj",'rb'))


school_order_count_by_month = {}
for month,mobile_order_count in mobile_order_count_by_month.items():
    school_order_count = {}
    for mobile,count in mobile_order_count.items():
        school = mobile_2_school.get(mobile, '')
        if not school:
            continue
        new_count = school_order_count.setdefault(school, 0) + count
        school_order_count[school] = new_count
    school_order_count_by_month[month] = school_order_count


w = Workbook()
title = (u'学校', u'单量')
for month, order_count in school_order_count_by_month.items():
    ws = w.add_sheet(month)
    ws.write(0, 0, u'学校')
    ws.write(0, 1, u'单量')
    row = 1
    for s,c in order_count.items():
        ws.write(row, 0, s)
        ws.write(row, 1, c)
        row += 1
w.save(u'学校单量按月份统计.xls')
