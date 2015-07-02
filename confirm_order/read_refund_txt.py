#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zh'
__date__ = '4/10/15'


refund_orders = open('refund_orders.txt', 'r')
for oid in refund_orders:
    print "'"+oid.strip()+"',"
