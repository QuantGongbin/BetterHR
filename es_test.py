from elasticsearch import Elasticsearch

es = Elasticsearch()

q = {
    "query" : {
        "match_all" : {}
    }
}
a = int(40)
print(a)
'''
result = es.count(index='betterknowledge', doc_type = 'knowledge', body=q)
max_length = result['count']
print(max_length)'''

