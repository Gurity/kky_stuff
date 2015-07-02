# -*- coding:utf-8 -*-

import requests
import json
from datetime import date, time, datetime, timedelta
from pymongo import MongoClient
import tablib

DB_NAME = 'wukong-release'
DB_URL = 'mongodb://sa:kuaikuaiyu1219@123.56.131.68:7900'

client = MongoClient(host=DB_URL)
db = client[DB_NAME]

def to_timestamp(the_time):
    #return (the_time - datetime.utcfromtimestamp(0)).total_seconds()
    return int((the_time - datetime.fromtimestamp(0)).total_seconds() * 1000.0)


def to_datetime(the_timestamp):
    return datetime.fromtimestamp(the_timestamp / 1000.0) # convert to local time
    #return datetime.utcfromtimestamp(the_timestamp) convert to utc time

#START_DATE = date.today() - timedelta(days=4)
#END_DATE = date.today()

if __name__ == '__main__':

    f = open('settings.txt', 'r')
    START_TIME = datetime.strptime(f.readline().replace('\n', ''), "%Y-%m-%d %H:%M:%S")
    END_TIME = datetime.strptime(f.readline().replace('\n', ''), "%Y-%m-%d %H:%M:%S")
    MARK_AS_PROCESSED = True if f.readline().replace('\n', '') == 'Y' else False
    f.close()

    headers = (
        '提现ID',
        '速递员ID',
        '速递员姓名',
        '速递员所属校区',
        '状态',
        '提现金额',
        '扣款金额',
        '实际支出',
        '提现时间',
        '提现方式',
        '[支付宝]收款账号',
        '[支付宝]支付宝姓名',
        '[支付宝]付款金额',
        '[支付宝]付款理由',
        '[银行]速递员姓名',
        '[银行]速递员手机号',
        '[银行]提现时间',
        '[银行]收款账号',
        '[银行]收款姓名',
        '[银行]备注',
        '[银行]收款银行',
        '[银行]收款银行支行',
        '[银行]收款省',
        '[银行]收款市'
    )

    data = []

    if MARK_AS_PROCESSED is True:

        db.withdraw.update({
            'created_time': {
                '$gt': to_timestamp(START_TIME),
                '$lt': to_timestamp(END_TIME)
            },
        }, {
            '$set': {
                'status': 'processed'
            }
        }, multi=True)

    withdraws = db.withdraw.find({
        'created_time': {
            '$gt': to_timestamp(START_TIME),
            '$lt': to_timestamp(END_TIME)
        },
    }).sort([('created_time', -1)])

    for withdraw in withdraws:
        expense = db.expend.find_one(
            {
                'withdraw_id': withdraw['_id']
            }
        )
        if expense:
            continue

        withdraw_id = str(withdraw['_id'])

        courier = db.courier.find_one({'_id': withdraw['courier_id']})

        if courier is None:
            continue

        courier_id = str(courier['_id'])

        courier_name = courier['name']

        courier_campus = courier['school']

        status = '已处理' if withdraw['status'] == 'processed' else '未处理'

        money = str(withdraw['money'] / 100.0)

        withdraw_time = str(to_datetime(withdraw['created_time']))

        withdraw_type = '支付宝' if withdraw['account_type'] == 'alipay' else '银行'

        alipay_account = withdraw['account'] if withdraw['account_type'] == 'alipay' else ''

        alipay_name = withdraw['name'] if withdraw['account_type'] == 'alipay' else ''

        alipay_money = str(withdraw['money'] / 100.0)

        alipay_note = '速递员提现'

        if withdraw['account_type'] == 'bank':

            bank_courier_name = courier_name

            bank_courier_mobile = courier['mobile']

            bank_withdraw_time = withdraw_time

            bank_account = withdraw['account'] if withdraw['account_type'] == 'bank' else ''

            bank_account_name = withdraw['name'] if withdraw['account_type'] == 'bank' else ''

            bank_note = '速递员提现'

            bank_name = withdraw['bank_name'] if withdraw['account_type'] == 'bank' else ''

            bank_branch = withdraw['bank_branch'] if withdraw['account_type'] == 'bank' else ''

            withdraw['bank_province_city'] = withdraw['bank_province_city'].encode('UTF-8')

            if '内蒙古' in withdraw['bank_province_city']:
            
                bank_province = '内蒙古'

            else:

                bank_province = withdraw['bank_province_city'].split('省')[0] if '省' in withdraw['bank_province_city'] else withdraw['bank_province_city'].split('市')[0]

            bank_city = withdraw['bank_province_city'].replace(bank_province, '').replace('省', '').replace('市', '')

            if bank_province in ['北京', '上海', '重庆', '天津']:
                bank_city = bank_province

        else:

            bank_courier_name = ''
            bank_courier_mobile = ''
            bank_withdraw_time = ''
            bank_account = ''
            bank_account_name = ''
            bank_note = ''
            bank_name = ''
            bank_branch = ''
            bank_province = ''
            bank_city = ''

        line = (
            withdraw_id,
            courier_id,
            courier_name,
            courier_campus,
            status,
            money,
            '0',
            money,
            withdraw_time,
            withdraw_type,
            alipay_account,
            alipay_name,
            alipay_money,
            alipay_note,
            bank_courier_name,
            bank_courier_mobile,
            bank_withdraw_time,
            bank_account,
            bank_account_name,
            bank_note,
            bank_name,
            bank_branch,
            bank_province,
            bank_city
        )

        data.append(line) 

    data = tablib.Dataset(*data, headers=headers)

    with open(('%s.xls' % str(datetime.now())).replace(':', '.'), 'wb') as f:
        f.write(data.xls)

