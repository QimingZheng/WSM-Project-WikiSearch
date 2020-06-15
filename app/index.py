# coding:utf-8

from flask import request
from flask import Flask,  render_template
from controller import search, getPage
import sys
import json
# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/')
def index():
    return "the server is running!"
   # return render_template('/result.html',name = 'zhangsan',)


@app.route('/search', methods=['GET'])
def do_search():
    print(request.args)
    params = {
        'query': request.args.get('query'),
        'method': request.args.get('method')
    }
    res = search(params)
    return json.dumps({
        'status': 1,
        'result': res['result'],
        'time': res['time']
    }, ensure_ascii=False)


@app.route('/page', methods=['GET'])
def page():
    docId = request.args.get('id')
    res = getPage(docId)
    return json.dumps({
        'status': 1,
        'page': res
    }, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
