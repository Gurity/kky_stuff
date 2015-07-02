__author__ = 'zh'
# -*- coding: utf-8 -*-

from xlwt import *
import pickle

record_file = open("record_dump.obj",'rb')
sales_record = pickle.load(record_file)
record_file.close()

item_sales = {
    # 'item_name': {
    #     'count': xxx
    #     'money': xxx
    # }
}

item_sales_1214 = {}

shop_item_sales = {
    # 'shop_name': {
    #     'item_name': {
    #         'count': xxx
    #         'money': xxx
    #     }
    # }
}

for r in sales_record:
    mobile = r[0]
    name = r[1]
    date = r[2]
    item_name = r[3]
    count = r[4]
    price = r[5]
    shop_name = r[6]
    if not shop_name:
        shop_name = mobile

    if date != '2014-12-24':
        item_record = item_sales.setdefault(item_name, {})
        item_record['count'] = item_record.get('count', 0) + int(count)
        item_record['money'] = item_record.get('money', 0.0) + float(price)
    else:
        item_record = item_sales_1214.setdefault(item_name, {})
        item_record['count'] = item_record.get('count', 0) + int(count)
        item_record['money'] = item_record.get('money', 0.0) + float(price)

    shop_record = shop_item_sales.setdefault(shop_name, {})
    shop_item = shop_record.setdefault(item_name, {})
    shop_item['count'] = shop_item.get('count', 0) + int(count)
    shop_item['money'] = shop_item.get('money', 0.0) + float(price)


title = (u'品名', u'销量', u'金额')
w = Workbook()
ws = w.add_sheet(u'销售统计(除12月24日)')
for colx, heading in enumerate(title):
    ws.write(0, colx, heading)

row = 1
total_count = 0
total_money = 0.0
for item_name, item_record in item_sales.items():
    ws.write(row, 0, item_name)
    ws.write(row, 1, item_record['count'])
    ws.write(row, 2, item_record['money'])
    total_count += item_record['count']
    total_money += item_record['money']
    row += 1
ws.write(row, 0, u'总计')
ws.write(row, 1, total_count)
ws.write(row, 2, total_money)

ws = w.add_sheet(u'12月24日')
row = 1
total_count = 0
total_money = 0.0
for item_name, item_record in item_sales_1214.items():
    ws.write(row, 0, item_name)
    ws.write(row, 1, item_record['count'])
    ws.write(row, 2, item_record['money'])
    total_count += item_record['count']
    total_money += item_record['money']
    row += 1
ws.write(row, 0, u'总计')
ws.write(row, 1, total_count)
ws.write(row, 2, total_money)

for shop_name, shop_record in shop_item_sales.items():
    ws = w.add_sheet(shop_name)
    for colx, heading in enumerate(title):
        ws.write(0, colx, heading)
    row = 1
    total_count = 0
    total_money = 0.0
    for item_name, item_record in shop_record.items():
        ws.write(row, 0, item_name)
        ws.write(row, 1, item_record['count'])
        ws.write(row, 2, item_record['money'])
        total_count += item_record['count']
        total_money += item_record['money']
        row += 1
    ws.write(row, 0, u'总计')
    ws.write(row, 1, total_count)
    ws.write(row, 2, total_money)

w.save('sales.xls')





































