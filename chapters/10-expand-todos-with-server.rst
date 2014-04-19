第十章 实战演练：扩展todos到Server端（backbonejs+webpy）
=======================================================================

上一节简单介绍了怎么使用webpy搭建一个后端的接口服务，这一节就来简单实现一下。

10.1 项目结构
------------------------------------
首先还是来看下项目的结构，然后再一步一步的分析，结构如下::

    src
    ├── index.html
    ├── init_sqlite.py
    ├── models.py
    ├── server.py
    ├── static
    │   ├── backbone.js
    │   ├── destroy.png
    │   ├── jquery.js
    │   ├── json2.js
    │   ├── todos.css
    │   ├── todos.js
    │   └── underscore.js
    └── todos.db

以上结构可以分为四个部分：模板、静态资源、后端逻辑处理、后端数据处理，其实最后两个都属于后端部分。

因为模板和静态资源和之前没有太大差异，因此合并在一起介绍。首先来看后端的接口。

10.2 后端接口
----------------------
相对于前端的各种model、collection和view，后端显得比较简单。只需要提供可访问的接口，并且根据POST、PUT、DELETE、GET这四种操作完成对数据库的CRUD即可（Create,Read,Update,Delete)。

先来看models中的代码，这里对todo表的操作进行了简单的封装:

.. code:: python

    #coding:utf-8
    import web

    db = web.database(dbn='sqlite', db="todos.db")

    class Todos(object):
        @staticmethod
        def get_by_id(id):
            return db.select('todos', where="id=$id", vars=locals())

        @staticmethod
        def get_all():
            return db.select('todos')

        @staticmethod
        def create(**kwargs):
            db.insert('todos', **kwargs)

        @staticmethod
        def update(**kwargs):
            db.update('todos', where="id=$id", vars={"id": kwargs.pop('id')}, **kwargs)

        @staticmethod
        def delete(id):
            db.delete('todos', where="id=$id", vars=locals())

代码很简单，从方法的命名上就知道要完成的功能是什么，这里不得不说一句，任何语言中好的变量或方法的命名，胜过大段的注释。

model部分没有具体的业务逻辑，只是针对数据库进行CRUD操作。下面来看给浏览器提供接口的部分。

server部分，提供了前端浏览器需要访问的接口，同时也提供了页面初始加载时的渲染页面的功能。server.py的代码如下:

.. code:: python

    #coding:utf-8
    import json

    import web
    from models import Todos
            
    urls = (
        '/', 'index',  #返回首页
        '/todo', 'todo',  #  处理POST请求
        '/todo/(\d*)', 'todo',  # 处理前端todo的请求,对指定记录进行操作
        '/todos/', 'todos',  # 处理前端todo的请求，返回所有数据
    )

    app = web.application(urls, globals())

    render = web.template.render('')

    # 首页
    class index:
        def GET(self):
            # 渲染首页到浏览器
            return render.index()

    class todo:
        def GET(self, todo_id=None):
            result = None
            itertodo = Todos.get_by_id(id=todo_id)
            for todo in itertodo:
                result = {
                    "id": todo.id,
                    "title": todo.title,
                    "order": todo._order,
                    "done": todo.done == 1,
                }
            return json.dumps(result)

        def POST(self):
            data = web.data()
            todo = json.loads(data)
            # 转换成_order, order是数据库关键字, sqlite3报错
            todo['_order'] = todo.pop('order')
            Todos.create(**todo)

        def PUT(self, todo_id=None):
            data = web.data()
            todo = json.loads(data)
            todo['_order'] = todo.pop('order')
            Todos.update(**todo)

        def DELETE(self, todo_id=None):
            Todos.delete(id=todo_id)


    class todos:
        def GET(self):
            todos = []
            itertodos = Todos.get_all()
            for todo in itertodos:
                todos.append({
                    "id": todo.id,
                    "title": todo.title,
                    "order": todo._order,
                    "done": todo.done == 1,
                })
            return json.dumps(todos)

    if __name__ == "__main__":
        app.run()
    
相对于model.py来说，这里做了些数据转换的操作，如前端backbone通过ajax发过来的数据需要转换之后才能存入数据库，而从数据库取出的数据也要稍加处理才能符合前端todos.js中定义的model的要求。

在这个server中，提供了三个四个url，依次功能为：首页加载、单个todo创建、单个todo查询修改和删除、查询全部。分成四个也主要是依据所选框架webpy的特性。

在url之后，是对应一个具体的class，url接受到的请求将有对应的class来处理，比如说 ``/todo`` 这个url，对应的处理请求的class就是todo。另外对应浏览器端发过来的POST、GET、PUT、DELETE请求，class对应的也是相应的方法。这也是选webpy的一个原因。

说我了后端提供的接口，以及如何进行处理的原理。我们来看如何修改前端的代码，才能让数据发送到后端来。

10.3 修改todos，发送数据到后端
--------------------------------------------
这个部分改动比较小，就不贴代码了。有需要的可以到 ``code`` 中看。

之前的数据是存在localstorage中，是因为引用了localStorage.js文件，并且在collection中声明了 ``localStorage: new Backbone.LocalStorage("todos-backbone")`` 。

在修改的时候有三个地方需要修改，第一是model的定义，部分代码：

.. code:: javascript

    var Todo = Backbone.Model.extend({
        urlRoot: '/todo',
        ......

第二个就是collection的修改，去掉了localStorage的声明，并添加url：

.. code:: javascript

    var TodoList = Backbone.Collection.extend({
        url: '/todos/',
        ......

这样就搞定了。

10.4 Demo的使用
----------------------------
在 ``code`` 中，如果想要把我的demo在本地运行的话，需要首先运行下 ``python init_sqlite.py`` 来初始化sqlite3的数据库，运行完之后会在本地生成一个todos.db的数据库文件。

之后，就可以通过运行 ``python server.py`` ，然后访问命令行提示的网址就可以使用了。



最后稍稍总结一下，我觉得到这一章为止，对技术比较认真、比较有追求的同学应该知道怎么通过backbonejs和webpy把前后端连起来了。所有的这些文章只是为了帮你打开一扇门，或者仅仅只是一盏灯，具体你的业务逻辑还是需要通过自己的思考来解决。妄图让别人帮你实现业务逻辑的人都是切实的不思上进的菜鸟。

另外，关于这个Todos的案例，是你在打算把Backbonejs应用于实践时必须要参考和思考的。虽然到网上搜罗一下 ``Backbonejs项目实例`` 比思考要省心，但是别人的始终是别人的，你不转化成自己的，始终无法灵活运用。借此告诫那些觉得这个Todo案例没啥用的同学们。



**导航**

* 上一章 09 `后端环境搭建：web.py的使用 <09-intro-webpy.rst>`_
* 下一章 11  `前后端实战演练：Web聊天室-功能分析 <11-web-chatroom-base-on-backbonejs-1.rst>`_
