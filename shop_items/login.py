from pymongo import MongoClient

#ali
host='mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin'
con=MongoClient(host=host)
db=con['nfw-release']

#back
#warning 110 is gone!schools and accounts db had dumped to ali host
#host_back = 'mongodb://192.168.1.110'
con_back = MongoClient(host=host)

host_self = 'mongodb://sa:kuaikuaiyu1219@localhost/admin'
con_self = MongoClient(host=host_self)
