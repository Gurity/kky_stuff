#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '5/8/15'


from pymongo import MongoClient
from bson import ObjectId


client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')

db_shark = client['shark-release']
db_wukong = client['wukong-release']

c_item = db_shark['item']
c_category = db_shark['category']
c_shop = db_shark['shop']
c_school = db_wukong['schools']

# school names to add special item
school_names = []
school_file = open('schools', 'r')
for s in school_file:
    school_names.append(s.strip())

school_names = [
    u'KKY大学主校区',
    u'远洋天地73号楼',
    u'快快鱼测试校区'
]

for school_name in school_names:
    school = c_school.find_one({'name':school_name})
    if not school:
        print 'no school: ', school_name
        continue

    cvs_shops = c_shop.find(
        {
            'type': 'cvs',
            'school_district': school['_id']
        }
    )
    for shop in cvs_shops:
        if u'烟店' in shop['name']:
            continue

        taocan_category = c_category.find_one(
            {
                'shop_id': shop['_id'],
                'name': u'套餐'
            }
        )
        if not taocan_category:
            result = c_category.insert(
                {
                    'shop_id': shop['_id'],
                    'priority': 1,
                    'name': u'套餐'
                }
            )
            category_id = result
        else:
            category_id = taocan_category['_id']

        item_info = {
            'shop_id': shop['_id'],
            'category': category_id,
            'id': int(2272),
            'name': u"[1分钱喝汇源]",
            'status': 'off_shelves',
            'price': int(1),
            'priority': int(20),
            'image_id': ObjectId("554cd10d38a212333ae1bd3e"),
            'description': u'新用户专享1盒'
        }

        result = c_item.insert(item_info)
        print result
