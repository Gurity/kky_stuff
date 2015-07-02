#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/8/15'


import datetime


def TimestampToText(timestamp):
    if timestamp == 0:
        return ''
    timestamp = int(timestamp/1000)
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y年%m月%d日 %H:%M:%S')

