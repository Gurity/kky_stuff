# -*- coding: utf-8 -*-
__author__ = 'zh'

import xlrd
import pickle


book = xlrd.open_workbook(file_contents=file(u"school_couriers_2.xls").read())
mobile2school = {}
for sheet_num in range(0, book.nsheets):
    sh = book.sheet_by_index(sheet_num)
    current_school = None
    for rx in range(2, sh.nrows):
        row = sh.row(rx)
        if u'混合' in sh.name:
            school = row[0].value
            mobile = row[2].value
        else:
            school = row[1].value
            mobile = row[3].value
        if not mobile:
            continue
        try:
            mobile = str(int(mobile))
        except:
            continue
        if school:
            current_school = school
        mobile2school[mobile] = current_school

    print 'ok'

record_dump = open('courier_school.obj', 'wb')
pickle.dump(mobile2school, record_dump)
record_dump.close()
