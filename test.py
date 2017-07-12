#import urllib
import requests
import json


def http_post():
    url = 'http://localhost:5000/'
    #url = 'http://10.0.0.12:5000'
    #url = 'http://49.65.1.250:8000'
    values = {
        "type":"query",
        "query_info":{
            "title":"医疗期工资支付标准",
            "num":20,
            "min":10
        }

    }

    res = requests.post(url, json=values)

    return json.loads(res.text)   #res.text  # 获取服务器返回的页面信息


resp = http_post()
print(resp)