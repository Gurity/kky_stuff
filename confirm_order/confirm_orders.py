#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import datetime
from bson import ObjectId
import DB
from redis import Redis
redis = Redis(db=13)
ACCESS_TOKEN = redis.get('__WUKONG_CLIENT_ACCESS_TOKEN__')
WUKONG_DB_NAME = 'wukong-release'
SHARK_DB_NAME = 'shark-release'
#MOBILE = "18814811677"

client = DB.getKKYClient()
WUKONG_DB = client[WUKONG_DB_NAME]
SHARK_DB = client[SHARK_DB_NAME]

courier_cls = WUKONG_DB['courier']
task_cls = WUKONG_DB['task']
subtask_cls = WUKONG_DB['subtask']
order_cls = SHARK_DB["order"]
bill_cls = WUKONG_DB['bill']
school_cls = WUKONG_DB['schools']

REFUND = [
    '551388af778d17053f1f6ce4',
    '55138968778d17053f1f6cf9',
    '55138a1f778d17053f1f6d14',
    '55140c59778d17053f1f7fd5',
    '55141211778d17053f1f8327',
    '55169415778d174819c08172',
    '5514d660778d1705507e9908',
    '5514d3d2778d1705507e98c8',
    '5513d5c5778d17053f1f72a0',
    '5517a8eb778d170537a75fc5',
    '551654fd778d170579eefc44',
    '551528bb778d1705507e9fad',
    '5516beea778d174819c091e7',
    '55155c41778d1705507eac55',
    '551789de778d170537a75bb5',
    '5517aa6b778d170537a75fe8',
    '5517bad5778d170537a762cc',
    '55157f4e778d1705507eb3b7',
    '5517e209778d170537a76aaa',
    '5517ebd1778d170537a76e2a',
    '5518bf28778d1704edd5c61e',
    '5518ae7a778d1704edd5c462',
    '5518bf74778d1704edd5c625',
    '551777b8778d170537a758a6',
    '551903b9778d1704edd5ce13',
    '5518c674778d1704edd5c6b8',
    '5518c525778d1704edd5c6b1',
    '550e2826778d1705220da5dd',
    '55190b6d778d1704edd5cfaa',
    '55190b07778d1704edd5cf90',
    '55160e76778d170579eef464',
    '55190fd2778d1704edd5d0e2',
    '55167b18778d170579ef01b1',
    '55180fb8778d170537a781f8',
    '551921ca778d1704edd5d4b1',
    '551920ce778d1704edd5d451',
    '55192b9d778d1704edd5d71f',
    '551777b3778d170537a758a5',
    '5517507e778d170537a75446',
    '55140ab6778d17053f1f7edc',
    '551940af778d1704edd5dfa0',
    '55194175778d1704edd5e016',
    '551944ff778d1704edd5e242',
    '55194ee4778d1704edd5ea96',
    '55190fd2778d1704edd5d0e2',
    '5513e65e778d17053f1f74cb',
    '55195a5c778d17042cda1738',
    '55169573778d174819c081f4',
    '5518efb9778d1704edd5cca1',
    '551a3000778d17476912094e',
    '551a279f778d1747691206f5',
    '551a26af778d174769120683',
    '551817f4778d170537a78411',
    '55194299778d1704edd5e0c6',
    '5519430f778d1704edd5e120',
    '551a65c6778d17476912124c',
    '550eb4bd778d1705220db25d',
    '5519e739778d17055a05aad0',
    '551a887c778d174769121eb7',
    '551a7736778d17476912181f',
    '551a929e778d1747691224d9',
    '551b439f778d173d163dc88f',
    '551aad5f778d17050dfc33a2',
    '5513feaf778d17053f1f7924',
    '551a5062778d174769120d0e',
    '551a6dad778d1747691214aa',
    '551a6e48778d1747691214e7',
    '551a6f3d778d17476912154f',
    '551b3bff778d173d163dc865',
    '551aa317778d17476912364e',
    '5517eab6778d170537a76dbc',
    '5517eb3b778d170537a76df7',
    '5517ebd1778d170537a76e2a',
    '551ba3be778d173d163dce36',
    '551ba348778d173d163dce22',
    '5517dfcb778d170537a76a28',
    '551a5aab778d174769120f7c',
    '551a7332778d1747691216bb',
    '551b9546778d173d163dcd5a',
    '551a767a778d1747691217e3',
    '551a774e778d17476912182e',
    '551a76d0778d174769121801',
    '551bb1ca778d173d163dcfe1',
    '551bad13778d173d163dcf38',
    '551ba956778d173d163dceda',
    '551ba57a778d173d163dce6d',
    '551ab53a778d174769124c51',
    '551bab55778d173d163dcf0b',
    '551bb532778d173d163dd085',
    '5517ba63778d170537a762a3',
    '5517bb3a778d170537a762e5',
    '551a929e778d1747691224d9',
    '551bb947778d173d163dd13a',
    '5517da36778d170537a76923',
    '551bd043778d173d163dd50c',
    '551bd8ad778d173d163dd6d7',
    '551bd4c7778d173d163dd5f0',
    '551bdb4c778d173d163dd799',
    '551bda47778d173d163dd74a',
    '551a7647778d1747691217c8',
    '551a75eb778d1747691217a6',
    '551be117778d173d163dd965',
    '551cbf36778d173bb399f715',
    '551a884c778d174769121ea2',
    '551a87d5778d174769121e3d',
    '551a874b778d174769121de2',
    '551cc154778d173bb399f78f',
    '551cd2fc778d1705234b2e76',
    '5520a47d778d170560f778f9',
    '551cc1cc778d173bb399f7a3',
    '551a8467778d174769121cb2',
    '551ceab7778d173bb399fbf4',
    '551ce798778d173bb399fba0',
    '551cee92778d173bb399fc41',
    '551beeee778d173d163dde2c',
    '551c9650778d1705234b1558',
    '551937c8778d1704edd5daee',
    '551aacc8778d17476912433c',
    '55167dbf778d170579ef020f',
    '551a94bc778d1747691226b8',
    '551953f5778d1704edd5f07b',
    '5519538a778d1704edd5eff4',
    '551952fa778d1704edd5ef19',
    '551bea32778d173d163ddc97',
    '551be000778d173d163dd925',
    '551bd4c7778d173d163dd5f0',
    '551ca86a778d17051e7aeabb',
    '551ca7f7778d17051e7aeab0',
    '551b98cc778d173d163dcd7d',
    '551ca182778d17051e7aea00',
    '551cb3ca778d1714797ad1ea',
    '55176f7c778d170537a7578b',
    '55176e74778d170537a75761',
    '551cbfff778d173bb399f751',
    '551ca884778d17051e7aeabe',
    '551bfaaf778d173d163de4eb',
    '551c0a69778d173d163deb4c',
    '551ca86a778d17051e7aeabb',
    '551c02e7778d173d163de933',
    '551cad56778d17051e7aeb13',
    '551bfdcf778d173d163de719',
    '551cbefc778d173bb399f706',
    '551d2703778d173bb33c7735',
    '551d2d74778d173bb36434aa',
    '551ab040778d174769124737',
    '551c7c61778d17051e7ae83a',
    '551d26a4778d173bb33c772c',
    '551d3a7b778d173bb364371e',
    '551e1caf778d17055e84e2ff',
    '551bcca5778d173d163dd47e',
    '551ded11778d17055e84dbf7',
    '551d4ebf778d173bb3ecdb7e',
    '551ce43d778d173bb399fb42',
    '551ce324778d173bb399fb36',
    '551cc94c778d173bb399f914',
    '551d4084778d173bb3643943',
    '551d1a87778d173bb33c7591',
    '551e07d3778d17055e84dfc8',
    '551e05ff778d17055e84df9e',
    '551e17ac778d17055e84e229',
    '551e1293778d17055e84e127',
    '551e21b8778d17055e84e39f',
    '551e1af1778d17055e84e2ba',
    '551c08ef778d173d163deb09',
    '551d1a87778d173bb33c7591',
    '551be502778d173d163ddaae',
    '551e2d62778d1764b4893a49',
    '55191ca1778d1704edd5d369',
    '55191ce9778d1704edd5d378',
    '551e12e5778d17055e84e131',
    '551cb1c5778d17051e7aeb41',
    '551a88c4778d174769121eed',
    '551bca04778d173d163dd418',
    '551f997f778d1704ea5f2af6',
    '551bc523778d173d163dd304',
    '551fb795778d1704ea5f2d50',
    '551fbbb8778d1704ea5f2dce',
    '551fc356778d1704ea5f2ec2',
    '551faa99778d1704ea5f2c42',
    '551e9cd2778d17441fc5f9be',
    '551e8f89778d17441fc5f337',
    '551fd533778d1704ea5f3228',
    '551e9d91778d17441fc5fa27',
    '551fc611778d1704ea5f2f2f',
    '5520bf4f778d170560f77b3c',
    '551bd5ad778d173d163dd624',
    '551fefc0778d1704ea5f38c9',
    '5520bd98778d170560f77b19',
    '551cb8cb778d1714790af40c',
    '551c1676778d173d163dec7f',
    '551f383d778d1704ea5f1ee3',
    '551f376a778d1704ea5f1ec5',
    '551f1c72778d1704ea5f1ccf',
    '551f4443778d1704ea5f212a',
    '551e2bcd778d176318b0d90a',
    '551e8db7778d17441fc5f242',
    '551f3b06778d1704ea5f1f51',
    '551f3eb6778d1704ea5f202e',
    '551d488a778d173bb3643c77',
    '551f5b8e778d1704ea5f2476',
    '551e8c39778d17441fc5f1ac',
    '551d16cd778d173bb33c753e',
    '551f4745778d1704ea5f21c1',
    '551f642a778d1704ea5f25bf',
    '551f5314778d1704ea5f23a3',
    '551ce4ee778d173bb399fb56',
    '551bbafb778d173d163dd16e',
    '551d1a31778d173bb33c7586',
    '551f68cc778d1704ea5f262b',
    '551e7a09778d17441fc5ed48',
    '551f6705778d1704ea5f260f',
    '551eb540778d17441fc5ffee',
    '551cc73f778d173bb399f8b5',
    '551ea96b778d17441fc5fe6e',
    '551f9657778d1704ea5f2ac5',
    '551fa2b1778d1704ea5f2baf',
    '551d0bc3778d173bb399ff6f',
    '551dfee8778d17055e84decb',
    '5520928a778d170560f777a4',
    '551a24e2778d1747691205e9',
    '551fd14d778d1704ea5f314d',
    '5520f53c778d170560f77e87',
    '551fe847778d1704ea5f36e5',
    '5520dd1d778d170560f77cb5',
    '55208044778d170560f77729',
    '551fd14d778d1704ea5f314d',
    '552108da778d170560f7807f',
    '552103d5778d170560f78012',
    '5520ef1c778d170560f77e2a',
    '55211b31778d170560f782f3',
    '55210e19778d170560f78109',
    '551f1c72778d1704ea5f1ccf',
    '55211f9f778d170560f78348',
    '551aa53a778d1747691238eb',
    '55211e5c778d170560f7832e',
    '552210c1778d1705519c1d89',
    '5522255f778d1705519c2077',
    '55221fbc778d1705519c1f80',
    '552238a5778d1705519c2313',
    '55223656778d1705519c2299',
    '55225ba7778d1705519c27e5',
    '552260e1778d1705519c28d4',
    '55223b20778d1705519c239f',
    '55225a53778d1705519c27bd',
    '552271ce778d1705519c2cdf',
    '552267b5778d1705519c2a2a',
    '551c0d5a778d173d163debc0',
    '55227eff778d1705519c3293',
    '551f3db2778d1704ea5f1fe2',
    '55213d1a778d170560f78722',
    '551ba939778d173d163dced7',
    '551d488a778d173bb3643c77',
    '551e08c2778d17055e84dfec',
    '5521e270778d1705519c1838',
    '55213e70778d170560f78772',
    '551e19cf778d17055e84e289',
    '551e10d5778d17055e84e0d4',
    '551d4888778d173bb3643c75',
    '551d49eb778d173bb3643cdc',
    '551d5934778d173bb3ecdf80',
    '5516c25a778d174819c0929c',
    '551d0179778d173bb399fe28',
    '551d151a778d173bb33c751a',
    '55167b18778d170579ef01b1',
    '5522419f778d1705519c24bb',
    '55213759778d170560f78605',
    '552246e3778d1705519c2552',
    '552390f9778d170fa24f3560',
    '551e79e4778d17441fc5ed39',
    '551bea32778d173d163ddc97',
    '5523871b778d170525596dbc',
    '5522a68b778d1705519c46ac',
    '55239530778d170fa24f3610',
    '55229f85778d1705519c451c',
    '552386fd778d170525596dba',
    '55229113778d1705519c3e22',
    '551d16cd778d173bb33c753e',
    '5522748e778d1705519c2e19',
    '551f460f778d1704ea5f2184',
    '55212581778d170560f78405',
    '551beebe778d173d163dde19',
    '55231fd3778d170525595fb0',
    '551e15d9778d17055e84e1b1',
    '551e7d00778d17441fc5edd4',
    '55238376778d170525596d3a',
    '55234888778d17052559647d',
    '55229d73778d1705519c4455',
    '5523af34778d170fa24f3c0c',
    '5523d543778d172a6138136a',
    '5523a2a5778d170fa24f3889',
    '5524aa5b778d170562aa9f57',
    '551bf9f9778d173d163de47c',
    '5523871b778d170525596dbc',
    '5522a68b778d1705519c46ac',
    '551a98fa778d174769122a49',
    '5523e5f8778d172a613820fd',
    '5523cb05778d172a61380dd7',
    '5524934c778d170562aa9a40',
    '551fd174778d1704ea5f3159',
    '55239530778d170fa24f3610',
    '551cc336778d173bb399f7eb',
    '5514d157778d1705507e9876',
    '551a9239778d174769122487',
    '552114b0778d170560f78208',
    '551a982a778d174769122943',
    '551a976b778d1747691228c6',
    '551a8201778d174769121bba',
    '5523ed24778d17250110a4fb',
    '551bab83778d173d163dcf0c',
    '551baa8a778d173d163dcefd',
    '5524e82b778d170562aaace4',
    '5521f6be778d1705519c1a9e',
    '55235d48778d17052559684c',
    '55236feb778d170525596b75',
    '552291aa778d1705519c3e7e',
    '55221ca9778d1705519c1ef2',
    '552525d4778d170562aac88e',
    '5524feeb778d170562aab281',
    '55214010778d170560f787bf',
    '551d4302778d173bb3643a62',
    '551d4302778d173bb3643a62',
    '551d22ac778d173bb33c76ca',
    '551d202f778d173bb33c7679',
    '551bfec6778d173d163de799',
    '551e839f778d17441fc5ef12',
    '552528d3778d170562aacbf3',
    '5523d4a3778d172a613812dc',
    '55253830778d170562aadfd9',
    '5523d069778d172a6138101e',
    '5525d7d1778d17054e6dcbc3',
    '5525d700778d17054e6dcb8f',
    '55251d79778d170562aac14e',
    '5525e1da778d17054e6dce47',
    '551fcc62778d1704ea5f3060',
    '552401d4778d17499f312d81',
    '5523c251778d172a61380a67',
    '5523c1e7778d172a61380a4a',
    '5524ac4f778d170562aaa010',
    '551bfc8c778d173d163de648',
    '5525fbb7778d17054e6dd5a1',
    '55211eb1778d170560f7833b',
    '5525110a778d170562aab9c5',
    '5525fc97778d17054e6dd627',
    '551ba3be778d173d163dce36',
    '551ba348778d173d163dce22',
    '551fa058778d1704ea5f2b71',
    '551fc471778d1704ea5f2ee8',
    '551fc411778d1704ea5f2ed7',
    '551aa8cc778d174769123dd3',
    '551aa76e778d174769123bc9',
    '55211322778d170560f781ce',
    '55196219778d1704edd6021b',
    '551bfac3778d173d163de4f8',
    '552252be778d1705519c26cc',
    '551f5b7a778d1704ea5f2472',
    '552386be778d170525596db6',
    '55251fbd778d170562aac302'
]

def CheckSubtaskBillValidation(subtask):
    subtask_id = subtask['_id']
    bills = list( bill_cls.find({"subtask_id": subtask_id}) )
    if len(bills) == 2:
        have_order_fee = False
        have_subtask_fee = False
        for bill in bills:
            if bill['type'] == 'order_fee':
                have_order_fee = True
            elif bill['type'] == 'subtask':
                have_subtask_fee = True
            else:
                print bill["_id"], bill['type']
        if have_subtask_fee or have_order_fee:
            return True
        else:
            return False

def CheckOrderValidation(order):
    if order['status'] in ['uncomment', 'done']:
        return True
    else:
        return False

def MarkOrderConfirm(order_id):
    condition = {"_id": ObjectId(order_id)}
    updater = {"$set": {"status": "uncomment"}}
    order_cls.update(condition, updater)


SCHOOL_NAMES = [
    u'丽江师范高等专科学校主校区',
    u'武汉东湖学院主校区',
    u'沈阳城市学院主校区',
    u'广东水利电力职业技术学院从化校区',
    u'中南大学南校区',
    u'潍坊科技学院主校区',
    u'盐城师范学院新长校区',
    u'云南农业大学主校区',

    u'云南大学旅游文化学院古城区校区',
    u'云南交通职业技术学院呈贡校区',
    u'大理学院主校区',
    u'河南农业大学许昌校区',
    u'河南工业职业技术学院新校区',
    u'河北科技师范学院开发区校区',
    u'河北科技师范学院秦皇岛校区',
    u'河北联合大学南校区',
    u'燕山大学里仁学院',
    u'河北联合大学轻工学院北校区',
    u'南华大学新校区',
    u'昆明理工大学呈贡校区',
    u'河北工业大学北辰校区',
    u'西藏大学林芝校区',
    u'武夷学院主校区',
    u'池州学院主校区'
]

SCHOOL_NAMES = [
    u'中南大学南校区'
]

for school_name in SCHOOL_NAMES:
    school = school_cls.find_one({'name':school_name})
    if not school:
        print school_name


schools = list(
    school_cls.find(
        { 'name': { '$in': SCHOOL_NAMES } }
    )
)
school_ids = [s['_id'] for s in schools]


STARTTIME = datetime.datetime(2015, 3, 29)
DEADLIME = datetime.datetime(2015, 4, 1)

#courier = courier_cls.find_one({"mobile": MOBILE})
tasks = list(
    task_cls.find({
        #"courier_id": courier["_id"],
        'status': {'$in': ['dispatched', 'processing', 'done']},
        "created_time": {
            "$gt": int( (STARTTIME - datetime.datetime.fromtimestamp(0)).total_seconds() * 1000 ),
            "$lt": int( (DEADLIME - datetime.datetime.fromtimestamp(0)).total_seconds() * 1000 )
        },
        '$or': [
            { 'district_id': { '$in': school_ids } },
            { 'district_name': { '$in': SCHOOL_NAMES } }
        ]
    })
)

print 'task count: ', len(tasks)

should_handle_subtasks = []
should_handle_orders = []


for task in tasks:
    subtasks = list( subtask_cls.find({"_id": {"$in": task['subtasks']}}) )
    for subtask in subtasks:
        if not CheckSubtaskBillValidation(subtask):
            should_handle_subtasks.append(subtask)

for subtask in should_handle_subtasks:
    order = order_cls.find_one({"_id": ObjectId(subtask['express_no'])})
    if order:
        if CheckOrderValidation(order):
            print "order %s is have been handled" % order['_id']
        elif str(order['_id']) not in REFUND:
            should_handle_orders.append(order)
    else:
        print "invalid order id %s" % subtask['express_no']

print 'order count: ', len(should_handle_orders)


APP_ID = "54d4e19b778d17046c86c8e6"
token = ACCESS_TOKEN
import requests
import json
WUKONG_SERVER = "https://wukong.kuaikuaiyu.com"
EXPRESS_DONE_URL = '%s/openapi.express.done' % WUKONG_SERVER
failed_orders = []
for order in should_handle_orders:
    trytime = 0
    while True:
        data = {
            "app_id": APP_ID,
            "subtask_id": order['express_id'],
            "subtask_coupon": order['items_price'],
            "access_token": token
        }
        response_text = requests.post(EXPRESS_DONE_URL, data=data, verify=False).text
        print order["_id"], response_text
        result = json.loads(response_text)
        if result['flag'] != 'error':
            MarkOrderConfirm(order["_id"])
            break
        elif trytime < 5:
            token = redis.get('__WUKONG_CLIENT_ACCESS_TOKEN__')
            trytime += 1
            print 'retry access token'
        else:
            failed_orders.append(order)
            break

    # flag = raw_input("Continue?")
    # if flag not in ['y']:
    #     exit()

pickle.dump(failed_orders, open('confirm_order_failed.obj', 'w'))
