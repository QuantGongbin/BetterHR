
from elasticsearch import Elasticsearch
import json
from jieba import analyse
import jieba
import requests


r = requests.get(url='http://49.65.1.250:8082/sysKnowledge/getSysKnowledges')
r.encoding = 'utf-8'
ans = json.loads(r.text)
data = ans['sysKnowledges']
#es = Elasticsearch()
#jieba.initialize()
tfidf = analyse.extract_tags
#print(data[0])

#test_data = data[0]
#qa_content = test_data['content']
#qa_keyword = tfidf(qa_content, withWeight=True)
#for keyword,weight in qa_keyword:
  #  weight2 = round(weight, 3)
    #print("关键字为%s,权重为%f" %(keyword, weight2))
  #  print(weight2)





for i in range(len(data)):
    qa_title = data[i]['titile']
    qa_topic = data[i]['topic']
    qa_category = data[i]['category']
    qa_content = data[i]['content']
    qa_id = int(data[i]['uuid'])
    qa_wordcnt = len(qa_content)
    qa_imgcnt = data[i]['imgCnt']
    qa_key = tfidf(qa_content, withWeight=True)
    qa_keyword = []
    qa_weight = []
    for word, weight in qa_key:
        qa_keyword.append(word)
        qa_weight.append(round(weight,3))
        #qa_keyword[word] = round(weight, 3)
    print("第%d个录入完成" % qa_id)
    #print(qa_title, qa_topic, qa_category, qa_content, qa_id, qa_wordcnt, qa_keyword, qa_weight)
    #print('\n')

    '''es.index(index="betterknowledge", doc_type="knowledge", id = qa_id,\
             body={"title": qa_title, "topic": qa_topic, "category": qa_category, \
                   "content": qa_content, "wordcnt": qa_wordcnt, "imgcnt":qa_imgcnt,\
                   "keyword": qa_keyword, "weight":qa_weight})'''







