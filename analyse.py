#此处分析category共有几种
#['劳动工资', '综合', ' 养老保险', '社会保险', '医疗保险', '生育保险', '劳动关系', '权益维护', '人事人才', '其他', '就业培训', '工伤保险']

import json
from jieba import analyse
import pandas
import requests

from elasticsearch import Elasticsearch

es = Elasticsearch()

query_string = '关于江苏省2017二建考试'
number = 40
min_query = 10
tfidf = analyse.extract_tags
query_keyword_list =  []
query_weight_list = []
query_list = ''

key_list = tfidf(query_string, withWeight=True)
for keyword, weight in key_list:
    query_keyword_list.append(keyword)
    query_weight_list.append(round(weight,3))
    query_list = query_list + keyword + ' '
#print(query_weight_list)
    ######构造查询体
q = {}
q['query'] = query = {}
query['match'] = match = {}
match['keyword'] = query_list
q['size'] = number
q['_source'] = ['title', 'keyword', 'weight']
#print(q)

result = es.search(index='betterknowledge', body=q)
#return_num = result['hits']['total']
#print(return_num)
result = result['hits']['hits']
#print("返回的结果长度为%d" % len(result))
query_return = {}
query_content = []
pd = pandas.DataFrame(index=range(len(result)), columns=['uuid', 'title', 'score'])
for t in range(len(result)):

    pd.at[t, 'uuid']= result[t]['_id']
    pd.at[t, 'title'] = result[t]['_source']['title']
    keywords = result[t]['_source']['keyword']
    weights = result[t]['_source']['weight']
    #print(weights)
    common_weight = set(keywords) & set(query_keyword_list)
    score = 0
    for k in common_weight:
        score += weights[keywords.index(k)] * query_weight_list[query_keyword_list.index(k)]
    pd.ix[t, 'score']= score
    pd = pd.sort_values(by='score', ascending=False)
    #query_content.append(q)
result_content = []
for t in range(number):
    q = {}
    q['uuid'] = pd.at[t, 'uuid']
    q['title'] = pd.at[t, 'title']
    result_content.append(q)
result = {
    "type":"query"
}
result['content'] = result_content
print(result)















