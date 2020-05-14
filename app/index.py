#coding:utf-8

from flask import request
from flask import Flask,  render_template
from spiderData import search_info

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/search.html')
   # return render_template('/result.html',name = 'zhangsan',)


@app.route('/search')
def search():
    keyword = request.args.get('wd')
    print (keyword)
    result, tim = search_info(keyword)
    return render_template('/result.html', data = result, num = len(result), tim = tim)



@app.route('/user/<name>')
def user(name):
    return '<h1>hello,%s!' % name

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
