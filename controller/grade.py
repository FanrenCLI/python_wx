from tornado.web import *
import itchat
import models.globaldata
from pymongo import *
import json
from utils.nosql import *
import time
import datetime
class GradeHandler(RequestHandler):
    '''
        argument:{stuid,pwd}
    '''
    def HandleWx2Json(self,handleString):
        listRes=handleString.split('⊙')[1:]
        backJson={}
        for i in listRes:
            temp=i.split( )
            backJson[temp[0]]=temp[1]
        return backJson 
    #添加一个处理get请求方式的方法
    def get(self):
        #参数传递
        stuid,pwd=self.get_argument("stuid","none"),self.get_argument("pwd","none")
        #查询数据库中是否存在此学号的成绩，用于接下来判断是全查询还是部分查询
        sqlGrade=NosqlUtil().selectByCondition('grade',{"stuid":stuid})
        #首先登录用户
        itchat.send_msg("DL "+stuid+" "+pwd, toUserName=models.globaldata.mps[0]['UserName'])
        #获取当前系统日期
        localtime=datetime.datetime.now().strftime('%Y-%m-%d')
        #判断数据库中是否存在此用户的相关信息
        if sqlGrade==None:
            # 全查询，先获取学号判断是大几的学生，推算入学年份
            gradeleve=int('20'+stuid[0:2])
            localYear=int(localtime[0:4])
            Result_Json={}
            for i in range(gradeleve,localYear):
                itchat.send_msg("CJCX1 "+str(i)+'-'+str(i+1)+'-1', toUserName=models.globaldata.mps[0]['UserName'])
                while True:
                    if models.globaldata.backmessage['Content'].find(str(i)+'-'+str(i+1)+'-1')!=-1:
                        Result_Json[str(i)+'-'+str(i+1)+'-1']=self.HandleWx2Json(models.globaldata.backmessage['Content'])
                        break
                itchat.send_msg("CJCX1 "+str(i)+'-'+str(i+1)+'-2', toUserName=models.globaldata.mps[0]['UserName'])
                while True:
                    if models.globaldata.backmessage['Content'].find(str(i)+'-'+str(i+1)+'-2')!=-1: 
                        Result_Json[str(i)+'-'+str(i+1)+'-2']=self.HandleWx2Json(models.globaldata.backmessage['Content'])
                        break
            Result_Json['stuid']=stuid
            NosqlUtil().insert("grade",Result_Json)
            del Result_Json["_id"]
        else:
            Result_Json={}
            #如果大于6月份，则认为是查询第一学期，否则就是第二学期
            if int(localtime[5:7])>6 and (localtime[0:4]+"-"+str(int(localtime[0:4])+1)+"-1" not in sqlGrade):
                itchat.send_msg("CJCX1 "+localtime[0:4]+"-"+str(int(localtime[0:4])+1)+"-1", toUserName=models.globaldata.mps[0]['UserName'])
                while True:
                    if models.globaldata.backmessage['Content'].find(localtime[0:4]+"-"+str(int(localtime[0:4])+1)+"-1")!=-1:
                        temp_Json=self.HandleWx2Json(models.globaldata.backmessage['Content'])
                        if temp_Json:
                            Result_Json[localtime[0:4]+"-"+str(int(localtime[0:4])+1)+"-1"]=temp_Json
                        break
            elif int(localtime[5:7])<=6 and (str(int(localtime[0:4])-1)+"-"+localtime[0:4]+"-2" not in sqlGrade):
                itchat.send_msg("CJCX1 "+str(int(localtime[0:4])-1)+"-"+localtime[0:4]+"-2", toUserName=models.globaldata.mps[0]['UserName'])
                while True:
                    if models.globaldata.backmessage['Content'].find(str(int(localtime[0:4])-1)+"-"+localtime[0:4]+"-2")!=-1: 
                        temp_Json=self.HandleWx2Json(models.globaldata.backmessage['Content'])
                        if temp_Json:
                            Result_Json[str(int(localtime[0:4])-1)+"-"+localtime[0:4]+"-2"]=temp_Json
                        break
            if Result_Json:
                NosqlUtil().UpdateByCondition("grade",{'stuid':stuid},Result_Json)
            Result_Json=dict(sqlGrade,**Result_Json)
            del Result_Json["_id"]
        del Result_Json["stuid"]
        self.write(Result_Json)