#encoding=utf8
__author__ = 'paul'
import json
import time
import xlrd
from login import con
import time
#from parseExcel import parseSchoolInfoFromEXL

db_name = 'shark-release'
db = con[db_name]
col_sch = db.school
col_shop = db.shop
col_cate = db.category
col_item = db.item_new
db_image = con['kuaikuaiyu-fs']
col_image = db_image['fs.files']

#city_price = './'
def parseSchoolInfoFromEXL(book):
    list_dic = []
    name = ['school', 'camp', 'num', 'pro', 'city', 'lng', 'lat', 'name', 'mobile', 'description']
    for shn in range(2):
        sh = book.sheet_by_index(shn)
        for ron in range(1,sh.nrows):
            row = sh.row(ron)
            dic = {}
            for i in range(len(name)):
                try:
                    if i == len(name)-2:
                        dic[name[i]] = str(int(row[i].value))
                    else:
                        dic[name[i]] = str(row[i].value)
                except Exception, e:
                    #print e
                    dic[name[i]] = row[i].value
                    if u'地址错误' in row[i].value:
                        dic['right_add'] = row[i+1].value
                        print row[i+1].value, 'ok'
            list_dic.append(dic)
    file('./schoolsData.json', 'wb').write(json.dumps(list_dic))
    info = json.loads(file('./schoolsData.json').read())
    print 'schoolsData:', len(info)
# dic_city_shopId
def parseCityShop():
    # parse excel
    # no school form school
    # dic_city_schID -> dic_city_shopID
    # ['school', 'camp', 'num', 'pro', 'city', 'lng', 'lat', 'name', 'mobile', 'description']
    dic_city_sch = {}
    dic_city_shopId = {}
    schs = json.loads(file('./schoolsData.json').read())
    for sch in schs:
        _schs = dic_city_sch.setdefault(sch.get('city'), [])
        school = sch.get('school')
        camp = sch.get('camp')
        if school and camp:
            cond = {
                'school': school,
                'camp': camp
            }
            scid = col_sch.find_one(cond)['_id']
            if scid not in _schs:
                _schs.append(scid)
    for city in dic_city_sch:
        shops = dic_city_shopId.setdefault(city, [])
        for sch in dic_city_sch[city]:
            for shop in list(col_shop.find({'school_district': sch})):
                shops.append(shop['_id'])
    #file('./cityShopId.json','wb').write(json.dumps(dic_city_shopId))
    #for each in dic_city_shopId:
       #print each,dic_city_shopId[each]
    return dic_city_shopId

    #book = xlrd.open_workbook(file_contents=file('./school_data.xls').read())
    #parseSchoolInfoFromEXL(book)
# parse excel: dic_city_items(id,price)
def parseCityItem():
    book = xlrd.open_workbook(file_contents=file('./city_price.xlsx').read())
    sh0 = book.sheet_by_index(0)
    dic_city_items = {}
    for i in range(1, sh0.nrows):
        row = sh0.row(i)
        _temp = []
        for j in range(4):
            _temp.append(row[j].value)
        items = dic_city_items.setdefault(_temp[1], [])
        _info = [int(_temp[2]), int(float(_temp[3])*100)]
        if _info not in items:
            items.append(_info)
    return dic_city_items
# dic_cate_brand_priority
def parseCategoryIndex():
    book = xlrd.open_workbook(file_contents=file('./category.xlsx').read())
    dic_cate_brand_priority = {}
    cats = [u'套餐', u'饮料', u'零食', u'速食', u'乳品', u'酒水', u'日用']
    name = ['order', 'brand']
    for shn in range(1, book.nsheets):
        #print 'sheet_num:', shn
        sh = book.sheet_by_index(shn)
        if cats[shn-1] in sh.name:
            dic_cate_brand_priority.setdefault(cats[shn-1], [])
            #                    dic_cate_brand_priority[cats[shn-1]]
            for rown in range(2, sh.nrows):
                row = sh.row(rown)
                dic = {}
                for i in range(len(name)):
                    dic[name[i]] = row[i].value
                dic_cate_brand_priority[cats[shn-1]].append(dic)
        else:
            print '!!!!:', sh.name
        print sh.name, ':', len(dic_cate_brand_priority[cats[shn-1]])
    return dic_cate_brand_priority
    #file('./cateBrandOrderData.json', 'wb').write(json.dumps(dic_cate_brand_priority))


# dic_id_info = {id: cate, brand, name,description} -> add priority
def parseItemInfo(dic_cate_brand_priority):
    book = xlrd.open_workbook(file_contents=file('./item_data.xlsx').read())
    sh0 = book.sheet_by_index(0)
    dic_id_info = {}
    for i in range(1, sh0.nrows):
        row = sh0.row(i)
        _temp = {}
        name = ['id', 'cate', 'brand', 'name', 'des']
        for j in range(5):
            _temp[name[j]] = (row[j].value)
        brand_prio = dic_cate_brand_priority.get(_temp['cate'])
        pp = 0
        for each in brand_prio:
            if each['brand'][:-1] == _temp['brand']:
                # if each['order'] == '' or None:
                #     print each['brand'],'!!!!!!!!!!!!!!'
                each['order'] += 0.001
                #print each['order']
                #_temp['priority']=each.get('order')
                pp = each.get('order')
                #print _info[4]
                #print _temp
        _temp['priority'] = pp
        dic_id_info[int(_temp['id'])] = _temp
    ii = 0
    for each in dic_id_info:
        if dic_id_info[each]:
            ll = len(dic_id_info[each])
        else:
            ll = 0
            print each, dic_id_info[each]
        if ll != 6:
            ii += 1
            print ii,each,dic_id_info[each]
    file('./itemIdInfo.json', 'wb').write(json.dumps(dic_id_info))
    return dic_id_info



# todo: item image change?

# insert item(price,name,des,id,shop_id,category,priority,image_id, status,created_time)
# dic_id_info ['id', 'cate', 'brand', 'name', 'des']
def insertItem(dic_city_shopId, dic_city_items, dic_id_info):
    ll_city = []
    ll_item = []
    dic_index = json.loads(file('./city_index.json').read())
    for city in dic_city_shopId:
        sids = dic_city_shopId.get(city)
        items = dic_city_items.get(city)
        if not items:
            _city = dic_index.get(city)
            items = dic_city_items.get(_city)
            if not items:
                ll_city.append(city)
                continue
        for sid in sids:
            for _item in items:
                id = _item[0]
                price = _item[1]
                item = dic_id_info.get(id)
                if not item:
                    ll_item.append(id)
                else:
                    cond = {}
                    cond = {
                        'name': item.get('name'),
                        'price': price,
                        'id': int(item.get('id')),
                        'description': item.get('des'),
                        'created_time': int(time.time()*1000),
                        'status': 'on_sale',
                        'priority': item.get('priority')
                    }
                    image_id = col_image.find_one({'filename':str(int(item.get('id')))})['_id']
                    cate = col_cate.find_one({'shop_id':sid,'name':item.get('cate')})['_id']
                    cond['category']= cate
                    cond['shop_id']= sid
                    cond['image_id']= image_id

                try:
                    col_item.insert(cond)
                except:
                    print cond
                    continue
    for i in ll_city:
        print i
    print ll_item
def main():
    dic_city_shopId = parseCityShop()
    dic_city_items = parseCityItem()
    dic_cate_brand_priority = parseCategoryIndex()
    dic_id_info = parseItemInfo(dic_cate_brand_priority)
    insertItem(dic_city_shopId, dic_city_items, dic_id_info)

main()

#detect if some hide sheet
def test(filename):
    book = xlrd.open_workbook(file_contents=file(filename).read())
    for i in range(book.nsheets):
        print i,book.sheet_by_index(i).name
#test('./city_price.xlsx')