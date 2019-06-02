from tornado.web import *
import tornado.ioloop
import threading
import time
import itchat
import sys
sys.path.append(r'F:\\python_work\\wx_backstage')
from controller.login import *
from controller.grade import *
import models.globaldata
#定义处理类型
def runbot():
    itchat.auto_login(hotReload=True)
    models.globaldata.mps = itchat.search_mps(name='南通大学教务学生管理系统')
    itchat.run()

@itchat.msg_register(itchat.content.TEXT, isMpChat=True)
def reply_msg(msg):
    models.globaldata.backmessage=msg

if __name__ == "__main__":
    threading.Thread(target=runbot).start()
    app = tornado.web.Application([(r'/hello',GradeHandler),
                                    (r'/login',loginHandler),
                                    (r'/login_wx',loginWxHandler)])
    #绑定一个监听端口
    app.listen(8888)
    #启动web程序，开始监听端口的连接
    tornado.ioloop.IOLoop.current().start()