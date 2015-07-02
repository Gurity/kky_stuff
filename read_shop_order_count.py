__author__ = 'zh'

from pymongo import MongoClient
import datetime
import pickle

def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6

start_time = int(totimestamp(datetime.datetime(2014, 8, 1, 0, 0))) * 1000
end_time = int(totimestamp(datetime.datetime(2015, 3, 1, 0, 0))) * 1000

client = MongoClient('mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin')
db = client['nfw-release']
c_order = db['order']
c_shop = db['shop']

shop_order_count_by_month = {}

for order in c_order.find({
    'created_time': { '$gt': start_time, '$lt': end_time },
    'status': { '$in': ['success', 'confirmed'] }
    }):
    shop_id = order.get('shop_id', '')
    timestamp = int(order['created_time'] / 1000)
    month = datetime.datetime.fromtimestamp(timestamp).month
    shop_order_count = shop_order_count_by_month.setdefault(month, {})
    count = shop_order_count.setdefault(shop_id, 0)
    shop_order_count[shop_id] = count + 1


record_dump = open('shop_order_count_by_month.obj', 'wb')
pickle.dump(shop_order_count_by_month, record_dump)
record_dump.close()