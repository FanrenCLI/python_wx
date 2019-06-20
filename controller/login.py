import itchat
import time
import json
from tornado.web import RequestHandler
from server.loginServer import *
from utils.sqlcon import *
import models.globaldata
class loginWxHandler(RequestHandler):
    def post(self):
        try:
            backinfo=get_user_info(self.get_argument("code","none"))
            flag= checkOpenid(backinfo["openid"])
            if flag:
                # 返回登录人的相关信息
                self.write(User(flag[1],flag[2],flag[3],flag[4]).__dict__)
            else:
                self.write("failure")
        except Exception:
            self.write("failure")

class loginHandler(RequestHandler):
    #添加一个处理get请求方式的方法
    def post(self):
        #向响应中，添加数据
        code,stuid,pwd=self.get_argument("code","none"),self.get_argument("id","none"),self.get_argument("pwd","none")
        if stuid=="none" or pwd=="none":
            return "failure"
        backinfo=get_user_info(code)
        itchat.send_msg("DL "+stuid+" "+pwd, toUserName=models.globaldata.mps)
        time.sleep(1)
        # 判断数据库中是否有此用户，若没有则进行以下操作，若有则直接返回用户信息
        Sqlresult=Sqlutils().selectByAccountPwd("userlist",stuid,pwd)
        flag= checkOpenid(backinfo["openid"])
        if Sqlresult:
            # 判断此用户是否绑定微信号，若有则直接返回用户数据，无则判断当前微信号是否已经存在，无则绑定
            if not Sqlresult[0][4] and not flag:
                Sqlutils().updateSelective("userlist",stuid,backinfo["openid"])
            self.write(User(Sqlresult[0][1],Sqlresult[0][2],Sqlresult[0][3],Sqlresult[0][4]).__dict__)
        else:
            # 没有此用户则，判断此账号和密码是否正确，正确则进行添加到数据库
            contain_username_str=models.globaldata.backmessage['Content'][0:10]
            userName=contain_username_str[3:contain_username_str.rfind(',')]
            if models.globaldata.backmessage['Content'][0:2]=="你好":
                # 判断当前微信号是否存在，
                if not flag:
                    AddUserInfo(userName,stuid,pwd,backinfo["openid"])
                    self.write(User(userName,stuid,pwd,backinfo["openid"]).__dict__)
                else:
                    AddUserInfo(userName,stuid,pwd,None)
                    self.write(User(userName,stuid,pwd,None).__dict__)
            else:
                self.write("failure")