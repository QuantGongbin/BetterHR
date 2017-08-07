import json
from flask import Flask
from flask import request
from flask import jsonify
from recall import callback
from error import err_callback
from flask import make_response
from flask_cors import *
import jieba
from jieba import analyse
from flask import current_app

jieba.initialize()

app = Flask(__name__)
CORS(app, supports_credentials = True)


@app.route('/', methods=['POST'])
def index():
    if not request.json:
        result = err_callback.err_json(type = 99)
        rst = make_response(jsonify(result))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        return rst, 201

    received = request.json
    if received['type'] == 'query':
        try:
            query_string = received['query_info']['title']
        except KeyError:
            result = err_callback.err_json(type = 1)
            rst = make_response(jsonify(result))
            rst.headers['Access-Control-Allow-Origin'] = '*'
            return rst, 201
        try:
            number = int(received['query_info']['num'])
        except ValueError:
            number = 20
        except KeyError:
            number = 20
        #print(current_app.max_length)
        result = callback.query_recall(current_app.tfidf, query_string, current_app.max_length, number, min)
        rst = make_response(jsonify(result))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        return rst, 201
    elif received['type'] == 'update':
        pass

@app.before_first_request
def init():
    #jieba.initialize()
    current_app.max_length = callback.get_max_length()
    #print(current_app.max_length)

    current_app.tfidf = analyse.extract_tags


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = False)
