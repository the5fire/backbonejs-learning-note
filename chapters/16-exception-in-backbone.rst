第十六章 补充异常处理
==============================

忘了之前定这么个题目是要表达什么内容，就简单介绍下wechat项目中的错误处理。


16.1 error的使用
---------------------------------

说这个错误处理其实很简单，有过JavaScript经验的同学应该看到Backbonejs中定义的回调函数选项中的error参数就知道怎么写了。

需要处理错误的场景都是在客户端和服务器端通信时，在wechat中主要是save和fetch时。有一段代码展示下就是:

.. code:: javascript

    registe: function(evt){
        var reg_username_input = $('#reg_username');
        var reg_pwd_input = $('#reg_pwd');
        var reg_pwd_repeat_input = $('#reg_pwd_repeat');
        var u = new User({
            username: reg_username_input.val(),
            password: reg_pwd_input.val(),
            password_repeat: reg_pwd_repeat_input.val(),
        });
        u.save(null, {
            success: function(model, resp, options){
                g_user = resp;
                // 跳转到index
                appRouter.navigate('index', {trigger: true});
            },
            error: function(model, resp, options) {
                alert(resp.responseText);
            }
        });
    },

这是用户注册时的代码，在save的参数的第二个参数部分添加了error的处理，具体功能就是alert出服务器端传回来的response的内容。

那么这么错误是什么时候触发的呢？正常情况下是触发success对应的function，那么什么是正常呢？正常和错误在Backbone.js中是通过返回的HTTP状态码来区分的（应该说是jQuery或者zepto这样下一层处理ajax的库），jQuery中错误判断的代码是这样的: ``if ( status >= 200 && status < 300 || status === 304 ) {`` 。

因此，对应着服务端的处理就是返回非20x 和304的错误就行，一般客户端的错误都会返回400（40x系列）这样的错误，服务器端的错误一般都是500以上的错误。

对应上面的的错误，服务器端在使用web.py框架要这么处理:

.. code:: python

    def POST(self):
        data = web.data()
        data = json.loads(data)
        username = data.get("username")
        password = data.get("password")
        password_repeat = data.get("password_repeat")

        if password != password_repeat:
            # 会返回HTTP400的错误，内容是message的内容
            raise web.BadRequest(message='两次密码输入不一致')

        user_data = {
            "username": username,
            "password": sha1(password),
            "registed_time": datetime.now(),
        }

        try:
            user_id = User.create(**user_data)
        except sqlite3.IntegrityError:
            raise web.BadRequest(message="用户名已存在!")

        user = User.get_by_id(user_id)
        session.login = True
        session.user = user

        result = {
            'id': user_id,
            'username': username,
        }
        return json.dumps(result)

这样就ok了。看起来都是基本的东西。


参考： `HTTP状态码 <http://zh.wikipedia.org/zh-cn/HTTP%E7%8A%B6%E6%80%81%E7%A0%81>`_


**导航**

* 上一章 15  `引入requirejs <15-import-requirejs.rst>`_
* 下一章 17  `自定义Backbonejs <17-customize-backbonejs-sync.rst>`_
