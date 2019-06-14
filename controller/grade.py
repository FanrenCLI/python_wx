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
        print(handleString)
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
            for i in range(gradeleve,localYear+1):
                itchat.send_msg("CJCX1 "+str(i)+'-'+str(i+1)+'-1', toUserName=models.globaldata.mps[0]['UserName'])
                Result_Json=dict(self.HandleWx2Json(models.globaldata.backmessage['Content']),**Result_Json) 
                itchat.send_msg("CJCX1 "+str(i)+'-'+str(i+1)+'-2', toUserName=models.globaldata.mps[0]['UserName'])
                Result_Json=dict(self.HandleWx2Json(models.globaldata.backmessage['Content']),**Result_Json) 
            NosqlUtil().insert('grade',Result_Json)
        else:
            Result_Json=sqlGrade
            #如果大于6月份，则认为是查询第一学期，否则就是第二学期
            if int(localtime[5:7])>6:
                itchat.send_msg("CJCX1 "+str(int(localtime[0:4])-1)+"-"+localtime[0:4]+"-2", toUserName=models.globaldata.mps[0]['UserName'])
                Result_Json=dict(self.HandleWx2Json(models.globaldata.backmessage['Content']),**Result_Json) 
            else:
                itchat.send_msg("CJCX1 "+localtime[0:4]+"-"+str(int(localtime[0:4])+1)+"-1", toUserName=models.globaldata.mps[0]['UserName'])
                Result_Json=dict(self.HandleWx2Json(models.globaldata.backmessage['Content']),**Result_Json)
            NosqlUtil().UpdateByCondition('admin',{'stuid':stuid},Result_Json)
        self.write(Result_Json)