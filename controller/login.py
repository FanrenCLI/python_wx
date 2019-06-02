import itchat
import time
from tornado.web import RequestHandler
from server.loginServer import *
from utils.sqlcon import *
import models.globaldata
class loginWxHandler(RequestHandler):
    def post(self):
        try:
            code=self.get_argument("code","none")
            backinfo=get_user_info(code)
            flag= checkOpenid(backinfo["openid"])
            if flag:
                # 返回登录人的相关信息
                print(flag[4])
                self.write(str(flag))
            else:
                self.write("failure")
        except Exception:
            self.write("failure")
        # return result.json()

class loginHandler(RequestHandler):
    #添加一个处理get请求方式的方法
    def post(self):
        #向响应中，添加数据
        code,stuid,pwd=self.get_argument("code","none"),self.get_argument("id","none"),self.get_argument("pwd","none")
        if stuid=="none" or pwd=="none":
            return "failure"
        backinfo=get_user_info(code)
        itchat.send_msg("DL "+stuid+" "+pwd, toUserName=models.globaldata.mps[0]['UserName'])
        time.sleep(1)
        # 判断数据库中是否有此用户，若没有则进行以下操作，若有则直接返回用户信息
        Sqlresult=Sqlutils().selectByAccountPwd("userlist",stuid,pwd)
        if Sqlresult:
            self.write(str(Sqlresult))
        else:
            resultstr=models.globaldata.backmessage['Content'][0:10]
            reuslt1=resultstr[3:resultstr.rfind(',')]
            flag= checkOpenid(backinfo["openid"])
            if models.globaldata.backmessage['Content'][0:2]=="你好":
                # 下次写从这里开始
                if not flag:
                    AddUserInfo(reuslt1,stuid,pwd,backinfo["openid"])
            else:
                self.write("failure")