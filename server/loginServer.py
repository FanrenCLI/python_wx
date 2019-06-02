import requests
from utils.sqlcon import *
from models.user import *

def get_user_info(js_code):
    req_params = {
        "appid": 'wx3563eb654dd6f231',  # 小程序的 ID
        "secret": '7d4484b369bcf3cc301bb9f7884c6a4a',  # 小程序的 secret
        "js_code": js_code,
        "grant_type": 'authorization_code'
    }
    req_result = requests.get('https://api.weixin.qq.com/sns/jscode2session', 
                              params=req_params, timeout=3, verify=False)
    return req_result.json()
def checkOpenid(openid):
    result=Sqlutils().selectByOpenid("userlist",openid)
    if len(result)!=0:
        return result[0]
    else:
        return False 
def AddUserInfo(name,stuid,pwd,openid):
    Usermodel=User(name,stuid,pwd,openid)
    Sqlutils().insert("userlist",Usermodel)