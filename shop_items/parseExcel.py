#encoding=utf8
__author__ = 'paul'
import xlrd
import json
import os




#book = xlrd.open_workbook(file_contents=file('./school_data.xls').read())

list_dic = []
def parseSchoolInfoFromEXL(book):
    name = ['school', 'camp', 'num', 'pro', 'city', 'lng', 'lat', 'name', 'mobile', 'description']
    for shn in range(book.nsheets):
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


def test():
    for r,d,f in os.walk('/home/paul/work/code_self/code/orders/importYanFromExcel/data'):
        print f,d,r
#test()

#parseSchoolInfoFromEXL(book)
def parse():
    book = xlrd.open_workbook(file_contents=file('./city_index.xlsx').read())
    sh0 = book.sheet_by_index(0)
    dic = {}
    for i in range(1,sh0.nrows):
        temp = []
        row = sh0.row(i)
        for j in range(2):
            temp.append(row[j].value)
        dic[temp[0]]=temp[1]
    print len(dic), dic
    file('./city_index.json','wb').write(json.dumps(dic))

parse()

