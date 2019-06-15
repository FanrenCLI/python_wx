import pymongo
import models.globaldata
import string

class NosqlUtil():
    def __init__(self):
        self.client=None
        self.db=None
    def connection(self):
        if self.client==None:
            self.client=pymongo.MongoClient(models.globaldata.mongodburl)
    def insert(self,CollectionName,JsonEntity):
        self.connection()
        self.db=self.client.admin
        coll=self.db[CollectionName]
        coll.insert(JsonEntity)
        self.client.close()
    def selectByCondition(self,CollectionName,Condition):
        self.connection()
        self.db=self.client.admin
        coll=self.db[CollectionName]
        if Condition!=None:
            result=coll.find_one(Condition)
        else:
            result=coll.find()
        self.client.close()
        return result
    def UpdateByCondition(self,CollectionName,Condition,Info):
        '''
            CollectionName:集合名称\n
            Condition:匹配条件\n
            Info:更新的信息\n
        '''
        self.connection()
        self.db=self.client.admin
        coll=self.db[CollectionName]
        coll.update_one(Condition,{"$set":Info})
        self.client.close()