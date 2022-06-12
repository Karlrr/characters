from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# 코딩 시작

db.characterpost.update_one({'name':'하니'},{'$set':{'portrait':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoQUMvkmky18X2M9eXBCCAfPkiXYRlc9t6og&usqp=CAU'}})