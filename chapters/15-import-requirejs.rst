第十五章 引入requirejs
================================================

前面花了四章的时间完成了项目( `wechat <https://github.com/the5fire/wechat>`_ )的开发，并且也放到了线上。这篇来说说模块化的事情。

15.1 模块化的概念
------------------------------------

对于通常的网站来说，一般我们不会吧所有的js都写到一个文件中，因为当一个文件中的代码行数太多的话会导致维护性变差，因此我们常常会根据业务（页面）来组织js文件，比如全站都用到的功能，我就写一个base.js，只是在首页会用到的功能，就写一个index.js。这样的话我更改首页的逻辑只需要更改index.js文件，不需要考虑太多的不相关业务逻辑。当然还有很重要的一点是按需加载，在非index.js页面我就不需要引入index.js。

那么对于单页应用（SPA）来说要怎么做呢，只有一个页面，按照传统的写法，即便是分开多个文件来写，也得全部放到<script>标签中，由浏览器统一加载。如果你有后端开发经验的话，你会意识到，是不是我们可以像写后端程序（比如Python）那样，定义不同的包、模块。在另外的模块中按需加载（import）呢？

答案当然是可以。

在前端也有模块化这样的规范，不过是有两套：AMD和CMD。关于这俩规范的对比可以参考知乎上的问答 `AMD 和 CMD 的区别有哪些 <http://www.zhihu.com/question/20351507>`_ 。

按照AMD和CMD实现的两个可以用来做模块化的是库分别是：require.js和sea.js。从本章的题目可以知道我们这里主要把require.js引入我们的项目。 对于这两库我都做了一个简单的Demo，再看下面长篇代码之前，可以先感受下： `require.js Demo <../code/requirejs-demo>`_ 和 `sea.js Demo <../code/seajs-demo>`_ 。

15.2 简单使用require.js
-----------------------------------

要使用require.js其实非常简单，主要有三个部分：1. 页面引入require.js；2. 定义模块；3. 加载模块。我们以上面提到我做的那个demo为例：

*首先* - 页面引入

.. code:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>the5fire.com-backbone.js-Hello World</title>
    </head>
    <body>
        <button id="check">新手报到- requirejs版</button>
        <ul id="world-list">
        </ul>
        <a href="http://www.the5fire.com">更多教程</a>
        <script data-main="static/main.js" src="static/lib/require.js"></script>
    </body>
    </html>

上面的script的data-main定义了入口文件，我们把配置项也放到了入口文件中。
来看下入口文件:

.. code:: javascript

    require.config({
        baseUrl: 'static/',
        shim: {
            underscore: {
                exports: '_'
            },
        },
        paths: {
            jquery: 'lib/jquery',
            underscore: 'lib/underscore',
            backbone: 'lib/backbone'
        }
    });

    require(['jquery', 'backbone', 'js/app'], function($, Backbone, AppView) {
        var appView = new AppView();
    });

上面baseUrl部分指明了所有要加载模块的根路径，shim是指那些非AMD规范的库，paths相当于你js文件的别名，方便引入。

后面的require就是入口了，加载完main.js后会执行这部分代码，这部分代码的意思是，加载 ``jquery`` 、 ``backbone`` 、 ``js/app`` （这个也可通过paths来定义别名），并把加载的内容传递到后面的function的参数中。o

来看看js/app的定义。

*定义模块*

.. code:: javascript

    // app.js
    define(['jquery', 'backbone'], function($, Backbone) {
        var AppView = Backbone.View.extend({
            // blabla..bla
        });
        return AppView;
    });

    // 或者这种方式
    define(function(require, exports, module) {
        var $ = require('jquery');
        var Backbone = require('backbone');

        var AppView = Backbone.View.extend({
            // blabla..bla
        });
        return AppView;
    });

这两种方式均可，最后需要返回你想暴露外面的对象。这个对象（AppView）会在其他模块中 ``require('js/app')`` 时加载，就像上面一样。


15.3 拆分文件
--------------------------------

上一篇中我们写了一个很长的chat.js的文件，这个文件包含了所有的业务逻辑。这里我们就一步步来把这个文件按照require.js的定义拆分成模块。

上一篇是把chat.js文件分开来讲的，这里先来感受下整体代码:

.. code:: javascript

    $(function(){
        var User = Backbone.Model.extend({
            urlRoot: '/user',
        });

        var Topic = Backbone.Model.extend({
            urlRoot: '/topic',
        });

        var Message = Backbone.Model.extend({
            urlRoot: '/message',
        });

        var Topics = Backbone.Collection.extend({
            url: '/topic',
            model: Topic,
        });

        var Messages = Backbone.Collection.extend({
            url: '/message',
            model: Message,
        });

        var topics = new Topics;

        var TopicView = Backbone.View.extend({
            tagName:  "div class='column'",
            templ: _.template($('#topic-template').html()),

            // 渲染列表页模板
            render: function() {
            $(this.el).html(this.templ(this.model.toJSON()));
            return this;
            },
        });

        var MessageView = Backbone.View.extend({
            tagName:  "div class='comment'",
            templ: _.template($('#message-template').html()),

            // 渲染列表页模板
            render: function() {
            $(this.el).html(this.templ(this.model.toJSON()));
            return this;
            },
        });

        var UserView = Backbone.View.extend({
            el: "#user_info",
            username: $('#username'),

            show: function(username) {
                this.username.html(username);
                this.$el.show();
            },
        });

        var AppView = Backbone.View.extend({
            el: "#main",
            topic_list: $("#topic_list"),
            topic_section: $("#topic_section"),
            message_section: $("#message_section"),
            message_list: $("#message_list"),
            message_head: $("#message_head"),

            events: {
                'click .submit': 'saveMessage',
                'click .submit_topic': 'saveTopic',
                'keypress #comment': 'saveMessageEvent',
            },

            initialize: function() {
                _.bindAll(this, 'addTopic', 'addMessage');

                topics.bind('add', this.addTopic);

                // 定义消息列表池，每个topic有自己的message collection
                // 这样保证每个主题下得消息不冲突
                this.message_pool = {};

                this.message_list_div = document.getElementById('message_list');
            },

            addTopic: function(topic) {
                var view = new TopicView({model: topic});
                this.topic_list.append(view.render().el);
            },

            addMessage: function(message) {
                var view = new MessageView({model: message});
                this.message_list.append(view.render().el);
            },

            saveMessageEvent: function(evt) {
                if (evt.keyCode == 13) {
                    this.saveMessage(evt);
                }
            },
            saveMessage: function(evt) {
                var comment_box = $('#comment')
                var content = comment_box.val();
                if (content == '') {
                    alert('内容不能为空');
                    return false;
                }
                var topic_id = comment_box.attr('topic_id');
                var message = new Message({
                    content: content,
                    topic_id: topic_id,
                });
                self = this;
                var messages = this.message_pool[topic_id];
                message.save(null, {
                    success: function(model, response, options){
                        comment_box.val('');
                        // 重新获取，看服务器端是否有更新
                        // 比较丑陋的更新机制
                        messages.fetch({
                            data: {topic_id: topic_id},
                            success: function(){
                                self.message_list.scrollTop(self.message_list_div.scrollHeight);
                                messages.add(response);
                            },
                        });
                    },
                });
            },

            saveTopic: function(evt) {
                var topic_title = $('#topic_title');
                if (topic_title.val() == '') {
                    alert('主题不能为空！');
                    return false
                }
                var topic = new Topic({
                    title: topic_title.val(),
                });
                self = this;
                topic.save(null, {
                    success: function(model, response, options){
                        topics.add(response);
                        topic_title.val('');
                    },
                });
            },

            showTopic: function(){
                topics.fetch();
                this.topic_section.show();
                this.message_section.hide();
                this.message_list.html('');
            },

            initMessage: function(topic_id) {
                var messages = new Messages;
                messages.bind('add', this.addMessage);
                this.message_pool[topic_id] = messages;
            },

            showMessage: function(topic_id) {
                this.initMessage(topic_id);

                this.message_section.show();
                this.topic_section.hide();
                
                this.showMessageHead(topic_id);
                $('#comment').attr('topic_id', topic_id);

                var messages = this.message_pool[topic_id];
                messages.fetch({
                    data: {topic_id: topic_id},
                    success: function(resp) {
                        self.message_list.scrollTop(self.message_list_div.scrollHeight)
                    }
                });
            },

            showMessageHead: function(topic_id) {
                var topic = new Topic({id: topic_id});
                self = this;
                topic.fetch({
                    success: function(resp, model, options){
                        self.message_head.html(model.title);
                    }
                });
            },
        });


        var LoginView = Backbone.View.extend({
            el: "#login",
            wrapper: $('#wrapper'),
            
            events: {
                'keypress #login_pwd': 'loginEvent',
                'click .login_submit': 'login',
                'keypress #reg_pwd_repeat': 'registeEvent',
                'click .registe_submit': 'registe',
            },

            hide: function() {
                this.wrapper.hide();
            },

            show: function() {
                this.wrapper.show();
            },

            loginEvent: function(evt) {
                if (evt.keyCode == 13) {
                    this.login(evt);
                }
            },

            login: function(evt){
                var username_input = $('#login_username');
                var pwd_input = $('#login_pwd');
                var u = new User({
                    username: username_input.val(),
                    password: pwd_input.val(),
                });
                u.save(null, {
                    url: '/login',
                    success: function(model, resp, options){
                        g_user = resp;
                        // 跳转到index
                        appRouter.navigate('index', {trigger: true});
                    }
                });
            },

            registeEvent: function(evt) {
                if (evt.keyCode == 13) {
                    this.registe(evt);
                }
            },

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
                    }
                });
            },
        });

        var AppRouter = Backbone.Router.extend({
            routes: {
                "login": "login",
                "index": "index",
                "topic/:id" : "topic",
            },

            initialize: function(){
                // 初始化项目, 显示首页
                this.appView = new AppView();
                this.loginView = new LoginView();
                this.userView = new UserView();
                this.indexFlag = false;
            },

            login: function(){
                this.loginView.show();
            },

            index: function(){
                if (g_user && g_user.id != undefined) {
                    this.appView.showTopic();
                    this.userView.show(g_user.username);
                    this.loginView.hide();
                    this.indexFlag = true;  // 标志已经到达主页了
                }
            },

            topic: function(topic_id) {
                if (g_user && g_user.id != undefined) {
                    this.appView.showMessage(topic_id);
                    this.userView.show(g_user.username);
                    this.loginView.hide();
                    this.indexFlag = true;  // 标志已经到达主页了
                }
            },
        });

        var appRouter = new AppRouter();
        var g_user = new User;
        g_user.fetch({
            success: function(model, resp, options){
                g_user = resp;
                Backbone.history.start({pustState: true});

                if(g_user === null || g_user.id === undefined) {
                    // 跳转到登录页面
                    appRouter.navigate('login', {trigger: true});
                } else if (appRouter.indexFlag == false){
                    // 跳转到首页
                    appRouter.navigate('index', {trigger: true});
                }
            },
        }); // 获取当前用户
    });

上面三百多行的代码其实只是做了最基本的实现，按照上篇文章的介绍，我们根据User，Topic，Message，AppView，AppRouter来拆分。当然你也可以通过类似后端的常用的结构：Model， View，Router来拆分。

*User的拆分*

这个模块我打算定义用户相关的所有内容，包括数据获取，页面渲染，还有登录状态，于是有了这个代码：

.. code:: javascript

    // user.js
    define(function(require, exports, module) {
        var $ = require('jquery');
        var Backbone = require('backbone');
        var _ = require('underscore');

        var User = Backbone.Model.extend({
            urlRoot: '/user',
        });

        var LoginView = Backbone.View.extend({
            el: "#login",
            wrapper: $('#wrapper'),

            initialize: function(appRouter) {
                this.appRouter = appRouter;
            },
            
            events: {
                'keypress #login_pwd': 'loginEvent',
                'click .login_submit': 'login',
                'keypress #reg_pwd_repeat': 'registeEvent',
                'click .registe_submit': 'registe',
            },

            hide: function() {
                this.wrapper.hide();
            },

            show: function() {
                this.wrapper.show();
            },

            loginEvent: function(evt) {
                if (evt.keyCode == 13) {
                    this.login(evt);
                }
            },

            login: function(evt){
                var username_input = $('#login_username');
                var pwd_input = $('#login_pwd');
                var u = new User({
                    username: username_input.val(),
                    password: pwd_input.val(),
                });
                var self = this;
                u.save(null, {
                    url: '/login',
                    success: function(model, resp, options){
                        self.appRouter.g_user = resp;
                        // 跳转到index
                        self.appRouter.navigate('index', {trigger: true});
                    }
                });
            },

            registeEvent: function(evt) {
                if (evt.keyCode == 13) {
                    this.registe(evt);
                }
            },

            registe: function(evt){
                var reg_username_input = $('#reg_username');
                var reg_pwd_input = $('#reg_pwd');
                var reg_pwd_repeat_input = $('#reg_pwd_repeat');
                var u = new User({
                    username: reg_username_input.val(),
                    password: reg_pwd_input.val(),
                    password_repeat: reg_pwd_repeat_input.val(),
                });
                var self = this;
                u.save(null, {
                    success: function(model, resp, options){
                        self.appRouter.g_user = resp;
                        // 跳转到index
                        self.appRouter.navigate('index', {trigger: true});
                    }
                });
            },
        });

        var UserView = Backbone.View.extend({
            el: "#user_info",
            username: $('#username'),

            show: function(username) {
                this.username.html(username);
                this.$el.show();
            },
        });

        module.exports = {
            "User": User,
            "UserView": UserView,
            "LoginView": LoginView,
        };
    });

通过define的形式定义了User这个模块，最后通过module.exports暴露给外面User，UserView和LoginView。

*Topic模块*

同User一样，我们在这个模块定义Topic的Model、Collection和View，来完成topic数据的获取也最终渲染。

.. code:: javascript

    //topic.js
    define(function(require, exports, module) {
        var $ = require('jquery');
        var Backbone = require('backbone');
        var _ = require('underscore');

        var Topic = Backbone.Model.extend({
            urlRoot: '/topic',
        });

        var Topics = Backbone.Collection.extend({
            url: '/topic',
            model: Topic,
        });

        var TopicView = Backbone.View.extend({
            tagName:  "div class='column'",
            templ: _.template($('#topic-template').html()),

            // 渲染列表页模板
            render: function() {
            $(this.el).html(this.templ(this.model.toJSON()));
            return this;
            },
        });

        module.exports = {
            "Topic": Topic,
            "Topics": Topics,
            "TopicView": TopicView,
        }
    });

一样的，这个模块也对外暴露了Topic、Topics、TopicView的内容。

*message模块*

.. code:: javascript

    //message.js
    define(function(require, exports, module) {
        var $ = require('jquery');
        var Backbone = require('backbone');
        var _ = require('underscore');

        var Message = Backbone.Model.extend({
            urlRoot: '/message',
        });

        var Messages = Backbone.Collection.extend({
            url: '/message',
            model: Message,
        });

        var MessageView = Backbone.View.extend({
            tagName:  "div class='comment'",
            templ: _.template($('#message-template').html()),

            // 渲染列表页模板
            render: function() {
            $(this.el).html(this.templ(this.model.toJSON()));
            return this;
            },
        });
        module.exports = {
            "Messages": Messages,
            "Message": Message,
            "MessageView": MessageView,
        }
    });

最后也是对外暴露了Message、Messages和MessageView数据。

*AppView模块*

上面定义的都是些基础模块，这个模块我们之前也说过，可以称为“管家View”，因为它是专门用来管理其他模块的。

.. code:: javascript

    //appview.js
    define(function(require, exports, module) {
        var $ = require('jquery');
        var _ = require('underscore');
        var Backbone = require('backbone');
        var TopicModule = require('topic');
        var MessageModule = require('message');

        var Topics = TopicModule.Topics;
        var TopicView = TopicModule.TopicView;
        var Topic = TopicModule.Topic;

        var Message = MessageModule.Message;
        var Messages = MessageModule.Messages;
        var MessageView = MessageModule.MessageView;

        var topics = new Topics();

        var AppView = Backbone.View.extend({
            el: "#main",
            topic_list: $("#topic_list"),
            topic_section: $("#topic_section"),
            message_section: $("#message_section"),
            message_list: $("#message_list"),
            message_head: $("#message_head"),

            events: {
                'click .submit': 'saveMessage',
                'click .submit_topic': 'saveTopic',
                'keypress #comment': 'saveMessageEvent',
            },

            initialize: function() {
                _.bindAll(this, 'addTopic', 'addMessage');

                topics.bind('add', this.addTopic);

                // 定义消息列表池，每个topic有自己的message collection
                // 这样保证每个主题下得消息不冲突
                this.message_pool = {};

                this.message_list_div = document.getElementById('message_list');
            },

            addTopic: function(topic) {
                var view = new TopicView({model: topic});
                this.topic_list.append(view.render().el);
            },

            addMessage: function(message) {
                var view = new MessageView({model: message});
                this.message_list.append(view.render().el);
                self.message_list.scrollTop(self.message_list_div.scrollHeight);
            },

            saveMessageEvent: function(evt) {
                if (evt.keyCode == 13) {
                    this.saveMessage(evt);
                }
            },
            saveMessage: function(evt) {
                var comment_box = $('#comment')
                var content = comment_box.val();
                if (content == '') {
                    alert('内容不能为空');
                    return false;
                }
                var topic_id = comment_box.attr('topic_id');
                var message = new Message({
                    content: content,
                    topic_id: topic_id,
                });
                var messages = this.message_pool[topic_id];
                message.save(null, {
                    success: function(model, response, options){
                        comment_box.val('');
                        // 重新获取，看服务器端是否有更新
                        // 比较丑陋的更新机制
                        messages.fetch({
                            data: {topic_id: topic_id},
                            success: function(){
                                self.message_list.scrollTop(self.message_list_div.scrollHeight);
                                messages.add(response);
                            },
                        });
                    },
                });
            },

            saveTopic: function(evt) {
                var topic_title = $('#topic_title');
                if (topic_title.val() == '') {
                    alert('主题不能为空！');
                    return false
                }
                var topic = new Topic({
                    title: topic_title.val(),
                });
                self = this;
                topic.save(null, {
                    success: function(model, response, options){
                        topics.add(response);
                        topic_title.val('');
                    },
                });
            },

            showTopic: function(){
                topics.fetch();
                this.topic_section.show();
                this.message_section.hide();
                this.message_list.html('');

                this.goOut()
            },

            initMessage: function(topic_id) {
                var messages = new Messages;
                messages.bind('add', this.addMessage);
                this.message_pool[topic_id] = messages;
            },

            showMessage: function(topic_id) {
                this.initMessage(topic_id);

                this.message_section.show();
                this.topic_section.hide();
                
                this.showMessageHead(topic_id);
                $('#comment').attr('topic_id', topic_id);

                var messages = this.message_pool[topic_id];
                messages.fetch({
                    data: {topic_id: topic_id},
                    success: function(resp) {
                        self.message_list.scrollTop(self.message_list_div.scrollHeight)
                    }
                });
            },

            showMessageHead: function(topic_id) {
                var topic = new Topic({id: topic_id});
                self = this;
                topic.fetch({
                    success: function(resp, model, options){
                        self.message_head.html(model.title);
                    }
                });
            },

        });
        return AppView;
    });

不同于上面三个基础模块，这个模块只需要对外暴露AppView即可（貌似也就只有这一个东西）。

*AppRouter模块*

下面就是用来做路由的AppRouter模块，这里只是定义了AppRouter，没有做初始化的操作，初始化的操作我们放到app.js这个模块中，app.js也是项目运行的主模块。

.. code:: javascript

    // approuter.js
    define(function(require, exports, module) {
        var $ = require('jquery');
        var _ = require('underscore');
        var Backbone = require('backbone');
        var AppView = require('appview');
        var UserModule = require('user');
        var LoginView = UserModule.LoginView;
        var UserView = UserModule.UserView;

        var AppRouter = Backbone.Router.extend({
            routes: {
                "login": "login",
                "index": "index",
                "topic/:id" : "topic",
            },

            initialize: function(g_user){
                // 设置全局用户
                this.g_user = g_user;
                // 初始化项目, 显示首页
                this.appView = new AppView();
                this.loginView = new LoginView(this);
                this.userView = new UserView();
                this.indexFlag = false;

            },

            login: function(){
                this.loginView.show();
            },

            index: function(){
                if (this.g_user && this.g_user.id != undefined) {
                    this.appView.showTopic();
                    this.userView.show(this.g_user.username);
                    this.loginView.hide();
                    this.indexFlag = true;  // 标志已经到达主页了
                }
            },

            topic: function(topic_id) {
                if (this.g_user && this.g_user.id != undefined) {
                    this.appView.showMessage(topic_id);
                    this.userView.show(this.g_user.username);
                    this.loginView.hide();
                    this.indexFlag = true;  // 标志已经到达主页了
                }
            },
        });

        return AppRouter;
    });

同样，对外暴露AppRouter，主要供app.js这个主模块使用。

*app模块*

最后，让我们来看下所有js的入口：

.. code:: javascript

    // app.js
    define(function(require) {
        var $ = require('jquery');
        var _ = require('underscore');
        var Backbone = require('backbone');
        var AppRouter = require('approuter');
        var UserModule = require('user');

        var User = UserModule.User;

        var g_user = new User();
        var appRouter = new AppRouter(g_user);
        g_user.fetch({
            success: function(model, resp, options){
                g_user = resp;
                Backbone.history.start({pustState: true});

                if(g_user === null || g_user.id === undefined) {
                    // 跳转到登录页面
                    appRouter.navigate('login', {trigger: true});
                } else if (appRouter.indexFlag == false){
                    // 跳转到首页
                    appRouter.navigate('index', {trigger: true});
                }
            },
        }); // 获取当前用户
    });

这个模块中，我们通过require引入Approuter，引入User模块。需要注意的是，不同于之前一个文件中所有的模块可以共享对象的实例（如：g_user, appRouter），这里需要通过参数传递的方式把这个各个模块都需要的对象传递过去。同时AppRouter和User也是整个页面生存期的唯一实例。因此我们把User对象作为AppRouter的一个属性。在上面的AppRouter定义中，我们又吧AppRouter的实例传递到了LoginView中，因为LoginView需要对url进行变换。

*总结*

好了，我们总结下模块拆分的结构，还是来看下项目中js的文件结构::

    └── js
        ├── app.js
        ├── approuter.js
        ├── appview.js
        ├── backbone.js
        ├── jquery.js
        ├── json2.js
        ├── message.js
        ├── require.js
        ├── topic.js
        ├── underscore.js
        └── user.js 

15.4 用require.js加载
-------------------------------------------

上面定义了项目需要的所有模块，知道了app.js相当于程序的入口，那么要怎么在页面开始呢？

就像一开始介绍的require.js的用法一样，只需要在index.html中加入一个js引用，和一段定义即可:

.. code:: html

    // index.html
    <script data-main="/static/js/app.js" src="/static/js/require.js"></script>
    <script>
    require.config({
        baseUrl: '/static',
        shim: {
            underscore: {
                exports: '_'
            },
        },
        paths: {
            "jquery": "js/jquery",
            "underscore": "js/underscore", 
            "backbone": "js/backbone",

            "user": "js/user", 
            "message": "js/message",
            "topic": "js/topic",
            "appview": "js/appview",
            "approuter": "js/approuter",
            "app": "js/app",
        }
    });
    </script>

需要解释的是上面的那个 ``shim`` 的定义。因为underscore并不没有对AMD这样的模块规范进行处理，因此需要进行模块化处理，有两种方式：1.修改underscore的源码，加上 ``define(function(require, exports, module)`` 这样的定义；2. 采用requirejs提供的shim来进行处理。


15.5 捋捋结构
------------------------------

上面把文件拆分了一下，但是没有把template从页面提取出来。有兴趣的可以自己尝试下。最后我们来整理一下项目的结构。

.. image:: ../images/wechat-arch.png

具体的代码也可以到 `wechat <https://github.com/the5fire/wechat>`_ 中去看，在requirejs这个分支，代码中添加了socketio，但是对上面的介绍没有影响。



**导航**

* 上一章 14  `前后端实战演练：Web聊天室-前端开发 <14-web-chatroom-base-on-backbonejs-4.rst>`_
* 下一章 16  `补充异常处理 <16-exception-in-backbone.rst>`_
