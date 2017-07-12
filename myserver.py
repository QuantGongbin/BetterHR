import json
from flask import Flask
from flask import request
from flask import jsonify
from recall import callback
import jieba
from jieba import analyse
from flask import current_app

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    if not request.json:
        return '<h1>not json</h1>'

    received = request.json
    if received['type'] == 'query':

        query_string = received['query_info']['title']
        number = received['query_info']['num']
        min = received['query_info']['min']
        result = callback.query_recall(current_app.tfidf, query_string, number, min)
        return jsonify(result), 201
    elif received['type'] == 'update':
        pass

@app.before_first_request
def init():
    jieba.initialize()
    current_app.tfidf = analyse.extract_tags


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = False)
