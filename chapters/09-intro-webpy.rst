第九章 后端环境搭建：web.py的使用
=======================================================================

前面都是前端的一些内容，但是要想做出一个能用的东西，始终是不能脱离后端的。因此这一节主要介绍如何使用python的一个web框架webpy。我想读我这个教程的同学大多都是前端，对后端没有什么感觉。因此关于后端的介绍以能用为主，不涉及太多的后端的东西。

9.1 python是什么
----------------------
简单来说Python和JavaScript一样，是一个动态语言，运行在服务器端。语法类似于程序伪码，或者说类似于自然语言。过多的语法和关键字就不再介绍。只需要记住Python是用缩进来判断语法块的，不像js用大括号。

9.2 webpy是什么
----------------------
和Backbonejs是js的一个框架一样，webpy是python的一个简单的web开发的框架。可以通过简单的几行代码启动一个web服务（虽然只是输出helloworld ^_^）。用它可以简单的满足咱们的开发需求。

因为是基于Python的框架，因此需要先安装Python环境，具体怎么装就不细说了，到http://python.org/download/ 安装python2.7.6这个版本。

之后安装 `webpy <http://webpy.org/>`_ 官网的说明，通过命令安装webpy： ::
    
    pip install web.py 
    或者
    easy_install web.py

    注意：linux下非root用户需要sudo

9.3 来一个Helloworld
-----------------------------
安装好之后，直接把webpy网站上的那段代码，贴到的用编辑器打开的文件中，保存为server.py。webpy网站代码如下：

.. code:: python

    import web
        
    urls = (
        '/', 'index'
    )
    app = web.application(urls, globals())

    class index:
        def GET(self):
            return 'Hello, World!'

    if __name__ == "__main__":
        app.run() 

然后在server.py的同目录下执行::

    python server.py

之后命令行会输出::

    http://0.0.0.0:8080/ 

这个提示，现在你在浏览器访问 http://127.0.0.1:8080 ，就会看到熟悉的helloworld，是不是超级简单。

9.4 简单构建api接口
----------------------------
在上面代码的基础上，按照前面backboneModel的定义，我们需要一个todo这模型的对应的链接，这个链接应该返回json格式的数据。并且能够支持post、put、get、delete这四个请求。现在来看接口部分的代码：

.. code:: python

    #添加todo相关的urls
    urls = (
        '/', 'index',  #返回首页
        '/todo/(\d+)/', 'todo',  # 处理前端todo的请求,操作对应的todo
        '/todo/', 'todos',  # 处理前端todo的整体请求,主要是获取所有的todo数据
    )

.. code:: python

    #添加接口的处理代码
    class todo:
        def GET(self, todo_id=None):
            context = {
                "title": "下午3点,coding",
                "order": 0,
                "done": False,
            }
            return json.dumps(context)

    #处理整体的请求
    class todos:
        def GET(self):
            result = []
            result.append({
                "title": "下午3点,coding",
                "order": 0,
                "done": False,
            })
            return json.dumps(result)

添加完这部分代码之后，启动server.py。访问 http://localhost:8080/todo/ 就能看到数据了，这里只是实现了get方法，其他的方法在下一篇中介绍。

9.5 加入数据库sqlite
-------------------------------
关于数据存储部分，我们使用sqlite数据库。sqlite的好处就是不需要安装即可使用。这样可以省去在数据库安装方面的折腾。

sqlite的介绍就不多说了，感兴趣的同学想必已经在查sqlite相关的东西了。这里只是演示在webpy中如何操作sqlite。

具体依然看代码:

.. code:: python

    #使用sqlite3操作数据库
    import sqlite3
    conn = sqlite3.connect('todos.db')
    
    #把todo改为这样：
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

完整代码可以在 `code` 文件夹找到。使用时，先运行init_sqlite.py这个文件，会帮你创建一个sqlite的数据库，并且插入一条数据，然后运行server.py就可以在浏览器访问 http://localhost:8080/todo/ 或者http://localhost:8080/todo/1/ 看到输出数据了。

9.6 总结
-------------------------
这里打算用webpy+sqlite来完成后台主要是想到这个东西比Django+Mysql那一套搭建起来比较容易。有兴趣看Django后台搭建的可以看这篇文章： `django开发环境搭建及使用 <http://www.the5fire.com/10-django-dev-env.html>`_ 。

这里没有使用webpy自带的db模块进行数据的操作，主要是文档和案例都不全，并且源码看起来挺绕。用Python自带的模块显然操作起来有点笨拙，之后会对这个数据操作部分进行简单的封装。


**导航**

* 上一章 08 `实战演练：todos分析（三）总结 <08-backbonejs-todos-3.rst>`_
* 下一章 10  `实战演练：扩展todos到Server端（backbonejs+webpy） <10-expand-todos-with-server.rst>`_
