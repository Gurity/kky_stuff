#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.CRITICAL)
import xlwt
import json
import datetime
import requests
from pymongo import MongoClient
from bson import ObjectId
import pymongo.errors
from bson import Code
import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--debug', default='true')
options = parser.parse_args()[0]
DEBUG = True if options.debug == 'true' else False
print DEBUG

MONGO_URL = "mongodb://192.168.1.114/admin"

WUKONG_DB_NAME = "wukong-release"
SHARK_DB_NAME = "shark-release"
NEW_SHOP_DISTRICT_KEY = "school_district"
if DEBUG:
    NEW_SHOP_DISTRICT_KEY = "new_school_district"
    WUKONG_DB_NAME = "wukong-debug"
    SHARK_DB_NAME = "shark-debug"

INFO_TEMPLATE = """DEBUG: %(DEBUG)s
WUKONG_DB_NAME %(WUKONG_DB_NAME)s
SHARK_DB_NAME %(SHARK_DB_NAME)s
NEW_SHOP_DISTRICT_KEY %(NEW_SHOP_DISTRICT_KEY)s"""
INFO_VALUES = {
    "DEBUG": str(DEBUG),
    "WUKONG_DB_NAME": WUKONG_DB_NAME,
    "SHARK_DB_NAME": SHARK_DB_NAME,
    "NEW_SHOP_DISTRICT_KEY": NEW_SHOP_DISTRICT_KEY
}
print INFO_TEMPLATE % INFO_VALUES
flag = raw_input("Continue?Y/n ")
if flag not in ['y', 'Y']:
    exit(0)


client = MongoClient(host=MONGO_URL)
WUKONG_DB = client[WUKONG_DB_NAME]
SHARK_DB = client[SHARK_DB_NAME]

shop_cls = SHARK_DB['shop']
courier_cls = WUKONG_DB['courier']
wschool_cls = WUKONG_DB['schools']
sschool_cls = SHARK_DB['school']
merged_school_cls = WUKONG_DB['schools_new']

VALID_SHOPS = []
MATCH_MULTI_WUKONG_shopS_SHOPS = []
NOT_MATCH_WUKONG_shop_SHOPS = []
LOCATE_FAIL_SHOPS = []
SHARK_SCHOOL_SCHOOL_NOT_EXISTS_SHOPS = []


regions = {
    '北京大区': ['北京市'],
    '东北大区': ['黑龙江省', '吉林省', '辽宁省'],
    '华北大区': ['内蒙古自治区', '河北省', '天津市'],
    '华东大区': ['山东省', '江苏省', '安徽省', '上海市', '江西省', '浙江省', '福建省', '山西省'],
    '华中大区': ['河南省', '湖北省', '湖南省'],
    '华南大区': ['广西壮族自治区', '广东省', '海南省'],
    '西北大区': ['陕西省', '甘肃省', '新疆维吾尔自治区', '青海省', '宁夏回族自治区'],
    '西南大区': ['西藏自治区', '云南省', '四川省', '重庆省', '贵州省', '重庆市']
}

def GetLocationInfo(location):
    around_url = "http://api.map.baidu.com/geocoder/v2/?ak=235165bab456ccfd0ddaef71ae4a0c1b&location=%s,%s&output=json&pois=0"%(str(location[1]), str(location[0]))
    response = requests.get(around_url)
    around = json.loads(response.text)
    if'result' not in around:
        return None
    retval = {
        "province": around["result"]["addressComponent"]["province"],
        "city": around["result"]["addressComponent"]["city"],
        "district": around["result"]["addressComponent"]["district"],
        "address": around["result"]["addressComponent"]["street"]+around["result"]["addressComponent"]["street_number"],
    }
    for key in regions.keys():
        region_provinces = regions[key]
        if retval['province'].encode("UTF-8") in region_provinces:
            retval['region'] = key
            break
    if 'region' not in retval:
        logging.critical("invalid province name %s" % retval["province"])
    return retval


def DumpShops(shops, filename):
    if shops and isinstance(shops, list) and len(shops) > 0:
        book = xlwt.Workbook(encoding="UTF-8")
        sheet = book.add_sheet("sheet1")
        header = [
            ("_id", u"商店ID"),
            ("name", u"学校"),
            ("mobile", u"电话"),
        ]
        for i in range(len(header)):
            sheet.write(0, i, header[i][1])
        for i in range(len(shops)):
            shop = shops[i]
            for j in range(len(header)):
                value = shop[header[j][0]]
                if isinstance(value, ObjectId):
                    value = str(value)
                sheet.write(i+1, j, value)
        filename = filename+"-%s.xls" % datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        book.save(filename)
        return filename
    return None


def DumpNotMatchShops(shops):
    print DumpShops(shops, "NotMatchShops")


def DumpDuplicateShops(shops):
    print DumpShops(shops, "MultiMatchShops")


def DumpLocateFailShops(shops):
    print DumpShops(shops, "LocateFailShops")

def DumpSharkSchoolNotExistsShops(shops):
    print DumpShops(shops, "SharkSchoolNotExists")

def HandlerInvalidShops(valid_shops):
    valid_ids = [shop["_id"] for shop in valid_shops]
    condition = {"_id":{"$nin": valid_ids}}
    updater = {
        "$set": {
            "status": "invalid",
        }
    }
    shop_cls.update(condition, updater)

def HandleValidShops(shops):
    def UpdateShopSchoolDistrictId(shop, school_id):
        log_format = "update shop %(shop_id)s school id from %(old_id)s to %(new_id)s"
        value = {
            "shop_id": str(shop["_id"]),
            "old_id": str(shop["school_district"]),
            "new_id": str(school_id)
        }
        logging.info(log_format%value)
        condition = {"_id": shop["_id"]}
        updater = {"$set":{NEW_SHOP_DISTRICT_KEY: school_id}}
        shop_cls.update(condition, updater)
    merged_school_cls.drop()
    for shop in shops:
        if 'location' not in shop:
            LOCATE_FAIL_SHOPS.append(shop)
            continue
        location = GetLocationInfo(shop['location'])
        if location is None:
            LOCATE_FAIL_SHOPS.append(shop)
            continue
        s_school = sschool_cls.find_one({"_id": shop["school_district"]})
        name = ('%s%s'%(s_school['school'], s_school['camp'])).strip()
        w_school = wschool_cls.find_one({"name":{"$regex": "%s"%name}})
        if w_school is None:
            logging.critical("NotMatchShops %s %s" % ( str(shop["_id"]), name ) )
            continue
        new_school = {
            "_id": w_school["_id"], # to avoid update courier's school id
            "name": s_school["school"].strip(),
            "campus": s_school["camp"].strip(),
            "location": shop["location"],
            "address": location["address"],
            "region": location['region'],
            "province": location["province"],
            "city": location["city"]
        }
        try:
            merged_school_cls.insert(new_school)
            UpdateShopSchoolDistrictId(shop, w_school["_id"])
        except pymongo.errors.DuplicateKeyError:
            if u'烟' not in shop['name']:
                logging.critical("duplicate key error %s %s" % (str(w_school["_id"]), (new_school["name"]+new_school["campus"]).strip()))
            else:
                UpdateShopSchoolDistrictId(shop, w_school["_id"])




# should update shop.school_district

def Mergeshop():
    def CheckCouriers():
        mapper = Code('''function(){emit(this.district_id, 1);}''')
        reducer = Code('''function(key, vals){return vals.reduce(function(i, j){ return i+j;});}''')
        courier_cls.map_reduce(mapper, reducer, "CS")
        old_schools = list( WUKONG_DB['CS'].find() )
        for os in old_schools:
            osid = os['_id']
            old_school = wschool_cls.find_one({"_id": osid})
            new_school = WUKONG_DB['schools_new'].find_one({"_id": osid})
            if not old_school:
                logging.critical("old_school %s does not exists" % str(osid))
            elif not new_school:
                logging.critical("courier could not find new school %s" % str(osid))
            elif old_school['name'] != (new_school['name']+new_school['campus']):
                logging.critical("old_school and new_school does not match %s-%s-%s"%(str(osid), old_school['name'], new_school['name']))

    def CheckShops():
        shops = list( shop_cls.find({NEW_SHOP_DISTRICT_KEY:{"$exists": True}, "status":{"$ne":"invalid"}}) )
        valid_ids = [shop["_id"] for shop in VALID_SHOPS]
        for shop in shops:
            if shop["_id"] not in valid_ids:
                continue
            nsid = shop[NEW_SHOP_DISTRICT_KEY]
            new_school = merged_school_cls.find_one({"_id": nsid})
            if new_school:
                continue
            else:
                logging.critical("shop %s could not find school %s" % (str(shop["_id"]), str(shop[NEW_SHOP_DISTRICT_KEY])) )



    def GetMatchWukongshop(ss):
        name = '%s%s'%(ss['shop'], ss['camp'])
        if len(ws) == 0:
            print "%s does not have a match shop in wukong" % name.encode("UTF-8")
            return None
        elif len(ws) == 1:
            pass
        elif len(ws) > 1:
            print "DUPLICATE: "+"\t".join([name]+[s['name'] for s in ws]).encode("UTF-8")
        return ws[0]

    def CheckSharkshopLocation(shop):
        if 'location' not in shop:
            print ("%s %s does not have a location info" % (shop["_id"], shop['shop'])).encode("UTF-8")
            return False
        else:
            return True

    # shark_shops = list( shop_cls.find({"status": 'open'}) )
    shark_shops = list( shop_cls.find({}) )
    for shop in shark_shops:
        shark_school = sschool_cls.find_one({"_id": shop["school_district"]})
        if not shark_school:
            SHARK_SCHOOL_SCHOOL_NOT_EXISTS_SHOPS.append(shop)
            continue
        campus_name = shark_school["school"]+shark_school['camp']
        campus_name = campus_name.strip()
        wukong_shops = list( wschool_cls.find({"name": {"$regex": campus_name}}) )
        if len(wukong_shops) == 0:
            NOT_MATCH_WUKONG_shop_SHOPS.append(shop)
        elif len(wukong_shops) == 1:
            VALID_SHOPS.append(shop)
        else:
            MATCH_MULTI_WUKONG_shopS_SHOPS.append(shop)
    DumpNotMatchShops(NOT_MATCH_WUKONG_shop_SHOPS)
    DumpDuplicateShops(MATCH_MULTI_WUKONG_shopS_SHOPS)
    DumpSharkSchoolNotExistsShops(SHARK_SCHOOL_SCHOOL_NOT_EXISTS_SHOPS)
    HandlerInvalidShops(VALID_SHOPS)
    HandleValidShops(VALID_SHOPS)
    CheckCouriers()
    CheckShops()


if __name__ == "__main__":
    Mergeshop()
