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
        flag= checkOpenid(backinfo["openid"])
        if Sqlresult:
            if Sqlresult[0][4]!=None:
                self.write(str(Sqlresult))
            else:
                if not flag:
                    Sqlutils().updateSelective("userlist",stuid,backinfo["openid"])
        else:
            contain_username_str=models.globaldata.backmessage['Content'][0:10]
            userName=contain_username_str[3:contain_username_str.rfind(',')]
            if models.globaldata.backmessage['Content'][0:2]=="你好":
                if not flag:
                    AddUserInfo(userName,stuid,pwd,backinfo["openid"])
                else:
                    AddUserInfo(userName,stuid,pwd,None)
            else:
                self.write("failure")