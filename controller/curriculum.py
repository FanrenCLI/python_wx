from tornado.web import *
from models.curriculum import *
import itchat
import models.globaldata
from pymongo import *
from utils.nosql import *
from utils.sqlcon import *
import re
import json
class CurrHandler(RequestHandler):
    '''
     argument:stuid
    '''
    def get(self):
        stuid=self.get_argument('stuid','none')
        itchat.send_msg('KBCX1 '+stuid,toUserName=models.globaldata.mps)
        while True:
            if ("Content" in models.globaldata.backmessage) and models.globaldata.backmessage['Content'].find("课表如下")!=-1:
                break
        backinfo=models.globaldata.backmessage['Content'].split( )
        classname=backinfo[1]
        # 此处查询数据库中是否已经存在此班级的相关课表
        sqlcurr=Sqlutils().selectByClassName('curriculum',classname)
        if sqlcurr:
            currinfo=json.dumps(sqlcurr)
            self.write(currinfo)
        else:
            currinfo=backinfo[3:]
            insertinfo=[]
            for i in currinfo:
                if i.find('✤')!=-1:
                    temp=i.split(',',4)
                    temp1=re.split('\)|\(|节',temp[4])
                    insertinfo.append(curriculum(temp[0][1:],temp[1],temp[2],temp[3],temp1[0],temp1[1],classname).__dict__)
            # Sqlutils().insertManyinfo("curriculum",insertinfo)
            self.write(json.dumps(insertinfo,ensure_ascii=False))