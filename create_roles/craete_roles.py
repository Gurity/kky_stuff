#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '3/23/15'


from pymongo import MongoClient
from bson import ObjectId
import xlrd
import re


client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['console']

c_role = db['roles']
c_users = db['users']

roles = {}

book = xlrd.open_workbook(file_contents=file(u"roles.xls").read())
for sheet_num in range(0, book.nsheets):
    sh = book.sheet_by_index(sheet_num)
    row_roles = sh.row(0)
    for c in range(2, sh.ncols):
        title = row_roles[c].value
        role_name = title.split('|', 1)[1]
        role_text = title.split('|', 1)[0]
        role = roles.setdefault(role_name, {})
        role['name'] = role_name
        role['text'] = role_text
    privilege_group_text = ''
    for rx in range(1, sh.nrows):
        row = sh.row(rx)
        title = row[1].value
        privilege_text = title.split('|', 2)[0]
        privilege_name = title.split('|', 2)[1]
        privilege_group = title.split('|', 2)[2]
        if row[0].value:
            privilege_group_text = row[0].value
        print privilege_group_text
        for c in range(2, sh.ncols):
            flag = row[c].value
            if flag:
                role_title = row_roles[c].value
                role_name = role_title.split('|', 1)[1]
                role_text = role_title.split('|', 1)[0]
                role = roles.setdefault(role_name, {})
                role['name'] = role_name
                role['text'] = role_text
                privileges = role.setdefault('privileges', [])
                privileges.append(privilege_name)

for k,v in roles.items():
    role_data = {
        'name': v['name'],
        'text': v['text'],
        'privileges': v['privileges'],
        'status': 'normal'
    }
    result = c_role.insert(role_data)
    print result
