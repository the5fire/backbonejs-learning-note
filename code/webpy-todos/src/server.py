#coding:utf-8
import json

import web
from models import Todos
        
urls = (
    '/', 'index',  #返回首页
    '/todo/(\d+)/', 'todo',  # 处理前端todo的请求,对指定记录进行操作
    '/todos/', 'todos',  # 处理前端todo的请求，返回所有数据
)

app = web.application(urls, globals())

render = web.template.render('')

# 首页
class index:
    def GET(self):
        return render.index()

class todo:
    def GET(self, todo_id=None):
        result = None
        itertodo = Todos.get_by_id(id=todo_id)
        for todo in itertodo:
            result = {
                "title": todo.title,
                "order": todo._order,
                "done": todo.done == 1,
            }
        return json.dumps(result)

class todos:
    def GET(self):
        todos = []
        itertodos = Todos.get_all()
        for todo in itertodos:
            todos.append({
                "title": todo.title,
                "order": todo._order,
                "done": todo.done == 1,
            })
        return json.dumps(todos)

if __name__ == "__main__":
    app.run()
