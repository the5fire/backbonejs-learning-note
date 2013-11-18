#coding:utf-8

__author__  = 'the5fire'

import json

import web
from mako.template import Template

urls = (
    '/', 'index',
    '/man/', 'Man',
)

class index:
    def GET(self):
        t = Template(filename='02-backbonejs-model.html', input_encoding='utf-8')
        return t.render()

class Man:
    def GET(self):
        return json.dumps({"name":"the5fire-server", "age": 10})

    def POST(self):
        data = web.data()
        print data
        return "success"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
