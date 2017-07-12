import json
from jieba import analyse
import jieba
import requests
import pickle

r = requests.get(url='http://49.65.1.250:8082/sysKnowledge/getSysKnowledges')
r.encoding = 'utf-8'
ans = json.loads(r.text)
file_name = 'knowledge.json'
output = open(file_name, 'wb')

pickle.dump(ans, output)
output.close()

