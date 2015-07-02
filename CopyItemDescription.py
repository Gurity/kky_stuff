#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/9/15'


from pymongo import MongoClient

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')

db_shark = client['shark-release']

c_item = db_shark['item']
c_item_repo = db_shark['item_repo']
c_category = db_shark['category']

condition = {
    'description': ''
}
query = c_item.find(condition)
count = query.count()
for item in query:
    category = c_category.find_one(item['category'])
    if not category:
        continue
    if category['name'].strip() == u'烟':
        continue
    else:
        number = item.get('id', None)
        if number:
            repo_item = c_item_repo.find_one(
                { 'number': number }
            )
            result = c_item.update(
                { '_id': item['_id'] },
                {
                    '$set': {
                        'description': repo_item.get('description', '')
                    }
                }
            )
            print result
print 'end'