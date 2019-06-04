import pymysql
from models.globaldata import *
from utils.singleton import *

@singleton
class Sqlutils():
    def __init__(self):
        self.conn=None
        self.cur=None
    def connection(self):
        if not self.conn:
            self.conn=pymysql.Connect(host=host,port=port,user=userid,password=pwd,db=db)
        self.cur=self.conn.cursor()
    @classmethod
    def ConnClose(cls):
        if cls.conn:
            cls.conn.close()
    def selectAll(self,tablelist):
        self.connection()
        cur=self.cur
        sqlstr="select * from "+tablelist
        result=cur.execute(sqlstr).fetchall()
        cur.close()
        return result
    def selectByOpenid(self,tablelist,openid):
        self.connection()
        cur=self.cur
        sqlstr="select * from " +tablelist+" where openid="
        cur.execute(sqlstr+"%s",(openid))
        result=cur.fetchall()
        cur.close()
        return result
    def selectByAccountPwd(self,tablelist,stuid,userpwd):
        self.connection()
        cur=self.cur
        sqlstr="select * from "+tablelist+" where stuid="
        cur.execute(sqlstr+"%s",(stuid))
        result=cur.fetchall()
        cur.close()
        return result
    def updateSelective(self,tablelist,stuid,openid):
        self.connection()
        cur=self.cur
        sqlstr="update "+tablelist+" set openid=%s where stuid=%s"
        cur.execute(sqlstr,(openid,stuid))
        result=cur.fetchall()
        cur.close()
        return result
    def insert(self,tablelist,UserModel):
        self.connection()
        cur=self.cur
        cur.execute("insert into "+tablelist+"(name,stuid,password,openid) values('%s','%s','%s','%s')"%(UserModel.name,UserModel.stuid,UserModel.pwd,UserModel.openid))
        self.conn.commit()
        cur.close()
        return True
