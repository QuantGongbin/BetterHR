


def query_recall(tfidf, query_string, number=20,min_query=10):
    '''

    :param query_string: 传入需要查询的string
    :param number: 传入需要查询的数据
    :param min_query: 最小返回的数据
    :return:
    '''

    from jieba import analyse
    from elasticsearch import Elasticsearch
    import pandas

    recall_number = number * 2

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
    q['_source'] = ['title', 'keyword', 'weight']
    #print(q)

    es = Elasticsearch()
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
    return result