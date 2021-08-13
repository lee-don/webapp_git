import uuid
import time
import base64
import json

def get_a_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8')
    return r_uuid.replace('=', '')
# import MySQLdb

def whatnoon():
    curtime = time.localtime()
    hour = curtime.tm_hour
    if hour < 6:
        return '凌晨了，注意休息：'
    elif hour < 12:
        return '早上好：'
    elif hour < 19:
        return '下午好：'
    else:
        return '晚上好：'

def to_result_json(s,suc=True):
    stus = {'suc': suc, 'content': s}
    result = json.dumps(stus,ensure_ascii=False)  # 先把字典转成json
    result = result.encode("utf-8").decode("utf-8")
    result = result.replace('\\"','"')
    result = result.replace('"{',"{")
    result = result.replace('}"',"}")
    return result

def obj_to_json(o):
    s = json.dumps(o.__dict__,ensure_ascii=False)
    s = s.replace('\\"','"')
    s = s.strip('"')
    return s

def obj_to_result_json(o):
    return to_result_json(obj_to_json(o))
