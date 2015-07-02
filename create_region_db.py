#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '5/18/15'


from pymongo import MongoClient
from bson import ObjectId
import pickle

client = MongoClient('mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900/admin')

db_console = client['console-release']
c_region = db_console['regions']


REGIONS = [
    {
        'name': u'北京大区',
        'province': [
            {
                'name': u'北京市',
                'city': [
                ]
            }
        ]
    },
    {
        'name': u'东北大区',
        'province': [
            {
                'name': u'黑龙江省',
                'city': []
            },
            {
                'name': u'吉林省',
                'city': []
            },
            {
                'name': u'辽宁省',
                'city': []
            }
        ]
    },
    {
        'name': u'华北大区',
        'province': [
            {
                'name': u'内蒙古自治区',
                'city': []
            },
            {
                'name': u'河北省',
                'city': []
            },
            {
                'name': u'天津市',
                'city': []
            },
            {
                'name': u'山西省',
                'city': []
            }
        ]
    },
    {
        'name': u'华东大区',
        'province': [
            {
                'name': u'山东省',
                'city': []
            },
            {
                'name': u'江苏省',
                'city': []
            },
            {
                'name': u'安徽省',
                'city': []
            },
            {
                'name': u'上海市',
                'city': [ ]
            },
            {
                'name': u'江西省',
                'city': []
            },
            {
                'name': u'浙江省',
                'city': []
            },
            {
                'name': u'福建省',
                'city': []
            }
        ]
    },
    {
        'name': u'华中大区',
        'province': [
            {
                'name': u'河南省',
                'city': []
            },
            {
                'name': u'湖北省',
                'city': []
            },
            {
                'name': u'湖南省',
                'city': []
            }
        ]
    },
    {
        'name': u'华南大区',
        'province': [
            {
                'name': u'广西壮族自治区',
                'city': []
            },
            {
                'name': u'广东省',
                'city': []
            },
            {
                'name': u'海南省',
                'city': []
            }
        ]
    },
    {
        'name': u'西北大区',
        'province': [
            {
                'name': u'陕西省',
                'city': []
            },
            {
                'name': u'甘肃省',
                'city': []
            },
            {
                'name': u'新疆维吾尔自治区',
                'city': []
            },
            {
                'name': u'青海省',
                'city': []
            },
            {
                'name': u'宁夏回族自治区',
                'city': []
            }
        ]
    },
    {
        'name': u'西南大区',
        'province': [
            {
                'name': u'西藏自治区',
                'city': []
            },
            {
                'name': u'云南省',
                'city': []
            },
            {
                'name': u'四川省',
                'city': []
            },
            {
                'name': u'重庆市',
                'city': [  ]
            },
            {
                'name': u'贵州省',
                'city': []
            }
        ]
    }
]


def get_province(rname, pname):
    for region in REGIONS:
        if region['name'] == rname:
            for province in region['province']:
                if province['name'] == pname:
                    return province
    return None


FILE_REGIONS = pickle.load(open('/home/www/connew/settings/REGIONS.obj', 'r'))
for region_name in FILE_REGIONS.keys():
    region = FILE_REGIONS[region_name]
    for province_name in region.keys():
        province = region[province_name]
        new_province = get_province(region_name, province_name)
        if not new_province:
            new_province = get_province(u'华北大区', u'山西省')

        for city_name in province:
            new_province['city'].append(
                {
                    'name': city_name
                }
            )


for region in REGIONS:
    result = c_region.insert(region)
    print result
