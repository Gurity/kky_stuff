#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '6/18/15'


from pymongo import MongoClient
import pickle
import time

client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')

db_console = client['console-release']

c_user = db_console['users']
c_school_manager = db_console['school_manager']

users = list(c_user.find({}))
for u in users:
    if u['status'] != 'normal':
        continue

    roles = u['roles']
    region = u['region']
    province = u['province']
    city = u['city']
    school = u['school_name']

    if school == u'全部校区':
        continue

    school_id = u.get('school_id')
    if not school_id:
        continue

    result = c_school_manager.update(
        { 'school_id': school_id },
        {
            '$push': {
                'managers': {
                    'console_account': u.get('name', ''),
                    'realname': u.get('realname', ''),
                    'mobile': u.get('mobile', ''),
                    'created_time': u.get('created_time', int(time.time()*1000))
                }
            }
        },
        upsert=True
    )

    print school_id, result

    '''
    current_manager = c_school_manager.find_one(
        { 'school_id': school_id }
    )
    if not current_manager:
        result = c_school_manager.insert(
            {
                'school_id': school_id,
                'managers': {}
            }
        )
    '''
