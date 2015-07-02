#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/1/15'

import json
AREAS = json.loads(open('area.json').read())
provinces = AREAS['p']
for province in provinces:
    print province['n']
    cities = province['i']
    for city in cities:
        print '    ', city['n']
print AREAS
