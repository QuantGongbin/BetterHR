from elasticsearch import Elasticsearch
from error import err_callback

def query_recall(tfidf, query_string, max_length, number=20,min_query=10):
    '''

    :param query_string: 传入需要查询的string
    :param number: 传入需要查询的数据
    :param min_query: 最小返回的数据
    :return:
    '''

    from jieba import analyse
    from elasticsearch import Elasticsearch
    import pandas

    recall_number = int(number) * 2
    if recall_number > max_length:
        recall_number = max_length - 5

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
    q['size'] = recall_number
    q['_source'] = ['title', 'keyword', 'weight','content','category']
    #print(q)

    es = Elasticsearch()
    results = es.search(index='betterknowledge', body=q)
    #return_num = result['hits']['total']
    #print(return_num)
    if results['hits']['total'] == 0:
        return err_callback.err_json(type = 0)
        #return err_callback(type = )
    result = results['hits']['hits']

    #print("返回的结果长度为%d" % len(result))
    query_return = {}
    query_content = []
    pd = pandas.DataFrame(index=range(len(result)), columns=['uuid', 'title', 'score','content','category'])
    for t in range(len(result)):

        pd.at[t, 'uuid']= result[t]['_id']
        pd.at[t, 'title'] = result[t]['_source']['title']
        keywords = result[t]['_source']['keyword']
        weights = result[t]['_source']['weight']
        pd.at[t, 'content'] = result[t]['_source']['content']
        pd.at[t, 'category'] = result[t]['_source']['category']
        #print(weights)
        common_weight = set(keywords) & set(query_keyword_list)
        score = 0
        for k in common_weight:
            score += weights[keywords.index(k)] * query_weight_list[query_keyword_list.index(k)]
        pd.ix[t, 'score']= score
        pd = pd.sort_values(by='score', ascending=False)
        #query_content.append(q)
    result_content = []
    if len(result) < number:
        number = len(result)
    for t in range(number):
        q = {}
        q['uuid'] = pd.at[t, 'uuid']
        q['title'] = pd.at[t, 'title']
        q['category'] = pd.at[t, 'category']
        q['content'] = pd.at[t, 'content']
        result_content.append(q)
    result = {
        "type":"query",
        "status":"success",
        "number": number
    }
    result['content'] = result_content
    return result

def get_max_length():
    es = Elasticsearch()
    q = {
        "query": {
            "match_all": {}
        }
    }
    result = es.count(index='betterknowledge', doc_type='knowledge', body=q)
    max_length = result['count']
    return max_length