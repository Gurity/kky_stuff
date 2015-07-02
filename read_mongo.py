__author__ = 'zh'
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import datetime
import pickle

def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6

start_time = int(totimestamp(datetime.datetime(2014, 12, 23, 14, 6))) * 1000
end_time = int(totimestamp(datetime.datetime(2015, 1, 7))) * 1000

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['nfw-release']

c_order = db['order']
c_shop = db['shop']
c_item = db['item']
c_column = db['column']

bsu_shop_mobiles = [
    '18010046691',
    '15650719210',
    '18811720508',
    '17801038560',
    '18811760766',
    '18813031011'
]

bsu_shops = {}
for shop in c_shop.find({'mobile': {'$in': bsu_shop_mobiles}}):
    if shop.get('mobile', '') in bsu_shop_mobiles:
        bsu_shops[shop['_id']] = shop


succeed_orders = []
for order in c_order.find({
    'shop_id': { '$in': bsu_shops.keys() },
    'created_time': { '$gt': start_time, '$lt': end_time },
    'status': { '$in': ['success', 'confirmed'] }
    }):
    succeed_orders.append(order)


def get_item_type(item_id):
    column = c_column.find_one({'items': item_id})
    if column is None:
        return ''
    return column.get('name', '')


sales_record = []  # ('mobile', 'name', 'date', 'type', 'count', 'price', 'shop_name')

def get_item_name(id):
    item = c_item.find_one({'_id': id})
    if item and item.get('name'):
        return item['name']
    else:
        return u'没名商品'

for order in succeed_orders:
    shop = bsu_shops[order.get('shop_id', '')]
    if not shop:
        continue
    person_name = shop['withdraw'].get('name', '')
    mobile = shop['mobile']
    shop_name = shop.get('name', '')
    timestammp = int(order['created_time'] / 1000)
    date = datetime.datetime.fromtimestamp(timestammp).strftime('%Y-%m-%d')
    for item in order['items']:
        id = item['_id']
        name = get_item_name(id)
        count = int(item['num'])
        price = float(item['price'])
        total_price = float(count) * price
        #id_dict = {
        #    'item_id': id
        #}
        #item_type = get_item_type(id_dict)
        sales_record.append((mobile, person_name, date, name, count, total_price, shop_name))

record_dump = open('record_dump.obj', 'wb')
pickle.dump(sales_record, record_dump)
record_dump.close()

