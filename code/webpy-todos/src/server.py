#coding:utf-8
import json
import sqlite3

import web
        
urls = (
    '/', 'index',  #返回首页
    '/todo/(\d+)/', 'todo',  # 处理前端todo的请求,对指定记录进行操作
    '/todo/', 'todos',  # 处理前端todo的请求，返回所有数据
)

app = web.application(urls, globals())
conn = sqlite3.connect('todos.db')
sql_query = 'SELECT id, title, _order, done FROM todos '

# 首页
class index:
    def GET(self):
        return 'Hello, World!'

class todo:
    def GET(self, todo_id=None):
        cur = conn.cursor()
        cur.execute(sql_query + ' where id=?', (todo_id, ))
        todo = cur.fetchone()
        cur.close()
        # 先用这种比较傻的方式
        context = {
            "id": todo[0],
            "title": todo[1],
            "order": todo[2],
            "done": todo[3],
        }
        return json.dumps(context)

class todos:
    def GET(self):
        result = []
        cur = conn.cursor()
        cur.execute(sql_query)
        todos = cur.fetchall()
        cur.close()
        for todo in todos:
            result.append({
                "id": todo[0],
                "title": todo[1],
                "order": todo[2],
                "done": todo[3],
            })
        return json.dumps(result)

if __name__ == "__main__":
    app.run()
