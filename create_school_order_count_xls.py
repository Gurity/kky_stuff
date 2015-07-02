__author__ = 'zh'
# -*- coding: utf-8 -*-

from xlwt import *
import pickle

record_file = open("school_order_count.obj",'rb')
school_order_count = pickle.load(record_file)
record_file.close()


title = (u'学校', u'单量')
w = Workbook()
ws = w.add_sheet(u'学校单量统计')
for colx, heading in enumerate(title):
    ws.write(0, colx, heading)

row = 1
for school,count in school_order_count.items():
    ws.write(row, 0, school)
    ws.write(row, 1, count)
    row += 1

w.save('school_order_count.xls')
