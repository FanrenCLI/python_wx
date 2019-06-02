from tornado.web import *
import itchat
import models.globaldata
class GradeHandler(RequestHandler):
    #添加一个处理get请求方式的方法
    def get(self):
        #向响应中，添加数据
            itchat.send_msg(self.get_argument("stuid","none"), toUserName=models.globaldata.mps[0]['UserName'])
            itchat.send_msg(self.get_argument("time","none"), toUserName=models.globaldata.mps[0]['UserName'])
            while True:
                if models.globaldata.backmessage['Content'][0:2]=="你好":
                    backinfo=models.globaldata.backmessage['Content']
                    self.write(backinfo)
                    break