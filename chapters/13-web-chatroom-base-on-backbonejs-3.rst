第十三章 前后端实战演练：Web聊天室-服务器端开发
=======================================================================

在上一章中简单的进行了在开发中经常要经过的一个步骤——详细设计，在详细设计中定义了数据模型，有哪些接口，以及页面的长相。比较简单，并没有对服务器端Python项目的结构进行设计，也没有对前端文件的组织进行规划。但是这个详细设计的目的是达到了，在我个人的实际经验中，项目的开发很少有按照软件工程中的瀑布模型来做的。大部分都是明确阶段目标，然后开发，然后再次明确，再次开发，不断迭代。

因此说到前篇文章的目的也就是指导后端开发提供一个什么样的接口，输出什么样的数据结构。也是指导前端应该怎么获取数据。在日常工作中，设计到前后端甚至是服务器和客户端的这种模式也是一样，两方人员在项目初期只要协定好接口和数据结构就行，随着项目的进行不断的调整。当然这种情况是说内部人员之间的沟通，如果是和外部人员的沟通情况就不一样了。

回到正题，后端的开发主要功能是提供接口，要提供哪些接口一定定义好了，模型也建立好了，现在需要做的就是搭一个项目，实现接口。


13.1 项目结构
------------------------------

项目使用了webpy这个微型的python框架，项目结构是依然按照之前对todos进行服务器端扩展时的结构, `onlinetodos <https://github.com/the5fire/onlinetodos>`_  ::

    .
    ├── __init__.py
    ├── handlers.py
    ├── init_sqlite.py
    ├── models.py
    ├── server.py
    ├── static
    │   ├── css
    │   │   ├── body.css
    │   │   └── semantic.min.css
    │   ├── img
    │   │   └── bg.jpg
    │   └── js
    │       ├── backbone.js
    │       ├── jquery.js
    │       ├── json2.js
    │       └── underscore.js
    ├── templates
    │   └── index.html
    └── wechat.db 

可以先忽略其中的静态文件的部分，下一章实现的时候会进行调整。只说后端的实现，主要分为三个部分：server部分、handler部分、和models部分，也就是上面对应的名字，这些名字本身就说明了这部分的功能。server主要是启动一个web服务器，其中进行了url的定义，对应url接受到的请求会传递到handlers中对应的类方法中，在方法中会调用Models中的Model类来获取数据，然后再返回给客户端（浏览器）。

13.2 server部分详解
-----------------------------------

这部分功能上已经介绍了，这里贴出代码详细介绍:

.. code:: python

    #!/usr/bin/env python
    #coding:utf-8
    import web
    from web.httpserver import StaticMiddleware

    urls = (
        '/', 'IndexHandler',  # 返回首页
        '/topic', 'TopicHandler',
        '/topic/(\d+)', 'TopicHandler',
        '/message', 'MessageHandler',
        '/user', 'UserHandler',
        '/user/(\d+)', 'UserHandler',
        '/login', 'LoginHandler',
        '/logout', 'LogoutHandler',
    )

    app = web.application(urls, globals())
    application = app.wsgifunc(StaticMiddleware)

    if web.config.get('_session') is None:
        session = web.session.Session(
            app,
            web.session.DiskStore('sessions'),
            initializer={'login': False, 'user': None}
        )
        web.config._session = session

    from handlers import (  # NOQA
        IndexHandler, RegisteHandler,
        LoginHandler, LogoutHandler,
        TopicHandler, MessageHandler
    )


    def main():
        app.run()

    if __name__ == "__main__":
        main()

这里首先是定义了url对应的handlers中的类，然后通过webpy的静态文件Middleware来处理静态文件的请求，接着初始化了项目的session。最后从handlers中引入所有用到的Handler。这里需要注意的是，handlers的引入需要在session定义的下面，因为handlers中需要用到session。

13.3 handler中的逻辑
--------------------------------------------

这里面主要逻辑是处理来自浏览器对相应的url的请求，因为项目需要处理用户登录，因此要引入前面定义的session来保存用户的状态。

来看代码:

.. code:: python

    #coding:utf-8
    import copy
    import json
    import hashlib
    import sqlite3
    from datetime import datetime

    import web

    from models import Message, User, Topic

    session = web.config._session

    CACHE_USER = {}


    def sha1(data):
        return hashlib.sha1(data).hexdigest()


    def bad_request(message):
        raise web.BadRequest(message=message)


    # 首页
    class IndexHandler:
        def GET(self):
            render = web.template.render('templates/')
            return render.index()


    class UserHandler:
        def GET(self):
            # 获取当前登录的用户数据
            user = session.user
            return json.dumps(user)

        def POST(self):
            data = web.data()
            data = json.loads(data)
            username = data.get("username")
            password = data.get("password")
            password_repeat = data.get("password_repeat")

            if password != password_repeat:
                return bad_request('两次密码输入不一致')

            user_data = {
                "username": username,
                "password": sha1(password),
                "registed_time": datetime.now(),
            }

            try:
                user_id = User.create(**user_data)
            except sqlite3.IntegrityError:
                return bad_request('用户名已存在!')

            user = User.get_by_id(user_id)
            session.login = True
            session.user = user

            result = {
                'id': user_id,
                'username': username,
            }
            return json.dumps(result)


    class LoginHandler:
        def POST(self):
            data = web.data()
            data = json.loads(data)
            username = data.get("username")
            password = data.get("password")
            user = User.get_by_username_password(
                username=username,
                password=sha1(password)
            )
            if not user:
                return bad_request('用户名或密码错误！')

            session.login = True
            session.user = user
            result = {
                'id': user.get('id'),
                'username': user.get('username'),
            }
            return json.dumps(result)


    class LogoutHandler:
        def GET(self):
            session.login = False
            session.user = None
            session.kill()
            return web.tempredirect('/#login')


    class TopicHandler:
        def GET(self, pk=None):
            if pk:
                topic = Topic.get_by_id(pk)
                return json.dumps(topic)

            topics = Topic.get_all()
            result = []
            for t in topics:
                topic = dict(t)
                try:
                    user = CACHE_USER[t.owner_id]
                except KeyError:
                    user = User.get_by_id(t.owner_id)
                    CACHE_USER[t.owner_id] = user
                topic['owner_name'] = user.username
                result.append(topic)
            return json.dumps(result)

        def POST(self):
            if not session.user or not session.user.id:
                return bad_request('请先登录！')

            data = web.data()
            data = json.loads(data)

            topic_data = {
                "title": data.get('title'),
                "owner_id": session.user.id,
                "created_time": datetime.now(),
            }

            try:
                topic_id = Topic.create(**topic_data)
            except sqlite3.IntegrityError:
                return bad_request('你已创建过该名称!')

            result = {
                "id": topic_id,
                "title": topic_data.get('title'),
                "owner_id": session.user.id,
                "owner_name": session.user.username,
                "created_time": str(topic_data.get('created_time')),
            }
            return json.dumps(result)

        def PUT(self, obj_id=None):
            pass

        def DELETE(self, obj_id=None):
            pass


    class MessageHandler:
        def GET(self):
            topic_id = web.input().get('topic_id')
            if topic_id:
                messages = Message.get_by_topic(topic_id) or []
            else:
                messages = Message.get_all()

            result = []
            current_user_id = session.user.id
            for m in messages:
                try:
                    user = CACHE_USER[m.user_id]
                except KeyError:
                    user = User.get_by_id(m.user_id)
                    CACHE_USER[m.user_id] = user
                message = dict(m)
                message['user_name'] = user.username
                message['is_mine'] = (current_user_id == user.id)
                result.append(message)
            return json.dumps(result)

        def POST(self):
            data = web.data()
            data = json.loads(data)
            if not (session.user and session.user.id):
                return bad_request("请先登录！")

            message_data = {
                "content": data.get("content"),
                "topic_id": data.get("topic_id"),
                "user_id": session.user.id,
                "created_time": datetime.now(),
            }
            m_id = Message.create(**message_data)
            result = {
                "id": m_id,
                "content": message_data.get("content"),
                "topic_id": message_data.get("topic_id"),
                "user_id": session.user.id,
                "user_name": session.user.username,
                "created_time": str(message_data.get("created_time")),
                "is_mine": True,
            }
            return json.dumps(result)
 
别看代码这么多，所有的具体的Handler的处理逻辑都是一样的——接受post请求，验证用户状态，存储；或者是接受get请求，调用Model获取数据，组织成json，然后返回。相当简单了，对吧。

13.4 models中的实现
--------------------------------------

这部分功能就是现实数据库的增删改查，行为基本一致，因此提出一个基础类来完成基本的操作。如果基础类满足不了需求，需要在各子类中实现自己的逻辑。

来看下实现代码:

.. code:: python

    #coding:utf-8
    import web

    db = web.database(dbn='sqlite', db="wechat.db")


    class DBManage(object):
        @classmethod
        def table(cls):
            return cls.__name__.lower()

        @classmethod
        def get_by_id(cls, id):
            itertodo = db.select(cls.table(), where="id=$id", vars=locals())
            return next(iter(itertodo), None)


        @classmethod
        def get_all(cls):
            # inspect.ismethod(cls.get_all)
            return db.select(cls.table())

        @classmethod
        def create(cls, **kwargs):
            return db.insert(cls.table(), **kwargs)

        @classmethod
        def update(cls, **kwargs):
            db.update(cls.table(), where="id=$id", vars={"id": kwargs.pop('id')}, **kwargs)

        @classmethod
        def delete(cls, id):
            db.delete(cls.table(), where="id=$id", vars=locals())


    class User(DBManage):
        id = None
        username = None
        password = None
        registed_time = None

        @classmethod
        def get_by_username_password(cls, username, password):
            itertodo = db.select(cls.table(), where="username=$username and password=$password", vars=locals())
            return next(iter(itertodo), None)


    class Topic(DBManage):
        id = None
        title = None
        created_time = None
        owner = None


    class Message(DBManage):
        id = None
        content = None
        top_id = None
        user_id = None
        reply_to = None

        @classmethod
        def get_by_topic(cls, topic_id):
            return db.select(cls.table(), where="topic_id=$topic_id", vars=locals())

在操作的同时还是定义了模型的属性，不过目前并没有用的上，如果打算进一步抽象的话是要用到的。

13.5 总结
---------------------------

整个后端的实现并不复杂，只是简单的数据库CRUD操作，也没有进行更深一步的抽象，不过满足接口需求就好，等前端实现的时候可能需要调整。

这个项目已经托管在github上了: `wechat <https://github.com/the5fire/wechat>`_ ，欢迎围观以及贡献代码。

**导航**

* 上一章 12  `前后端实战演练：Web聊天室-详细设计 <12-web-chatroom-base-on-backbonejs-2.rst>`_
* 下一章 14  `前后端实战演练：Web聊天室-前端开发 <14-web-chatroom-base-on-backbonejs-4.rst>`_
