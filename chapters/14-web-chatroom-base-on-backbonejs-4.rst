第十四章 前后端实战演练：Web聊天室-前端开发
=======================================================================

在上一章的 `服务器端开发 <13-web-chatroom-base-on-backbonejs-3.rst>`_ 中我们定义了模型，实现了几个实体增删改查得功能，也提供了前端访问数据的接口。但在前端的实现过程中又对接口进行了调整，以更符合前端的使用。在真实的开发中也是如此，定义的接口合不合适只有在开发时才知道。

目前代码并没有进行模块的划分，在单js文件(chat.js)中实现了所有逻辑。下一步会进行通过seajs或者requirejs来进行模块管理。

关于前端样式的设计和开发并不在这个系列的计划中，因此就不多做介绍了，只是基于semantic进行了简单的设计，有兴趣的可以自己去看： `wechat项目 <https://github.com/the5fire/wechat>`_ 。

14.1 前端文件结构
-------------------------------------

前端的结构和前面的项目结构一样，只是添加了chat.js和自定义样式的chat.css文件，我们所有的代码都在这个文件中编写。

::

    ├── static
    │   ├── css
    │   │   ├── body.css
    │   │   ├── chat.css
    │   │   └── semantic.min.css
    │   ├── fonts
    │   │   ├── basic.icons.svg
    │   │   ├── basic.icons.woff
    │   │   ├── icons.svg
    │   │   └── icons.woff
    │   ├── img
    │   │   └── bg.jpg
    │   └── js
    │       ├── backbone.js
    │       ├── chat.js
    │       ├── jquery.js
    │       ├── json2.js
    │       └── underscore.js
    ├── templates
    │   └── index.html


14.2 Model和Collection定义
-----------------------------------

我们还是先来定义Model的实现，前端的Model应该和后端的Model定义一样，不然数据传递就会有问题。因为在后端已经明确定义了Model有哪些属性，这里的定义就简单多了。当然这也是动态语言的优势——动态的添加属性。

我们要定义三个Model和两个Collection，因为User这个对象在前端只会存在一份，不需要定义集合。来看具体实现:

.. code:: javascript

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

我们之定义了基本的属性，这些属性保证了我们可以可以直接通过collection或者model获取到后端的数据。

14.3 视图和模板的定义
--------------------------------------------

定义了基本的Model之后，就相当于是有了数据的获取方式，下一步就是如何显示这些数据了。因此就需要用Backbonejs中的view和template来定义我们的具体显示了。

首先来定义view:

.. code:: javascript

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

根据定义的三个Model，定义了把数据渲染到模板的方式，对应的模块是什么样的呢，我们来看下:

.. code:: html

    <script type="text/template" id="topic-template">
        <a href="#topic/<%= id %>">
            <div class="column">
                <div class="ui segment">
                    <h3><%= title %></h3>
                    <p>
                    创建者：<%= owner_name %>
                    </p>
                    <p>
                    创建时间：<%= created_time %>
                    </p>
                </div>
            </div>
        </a>
    </script>

    <script type="text/template" id="message-template">
        <div class="content <% if(is_mine) { %> right <% } %>" data="<%= id %>">
            <a class="author"><%= user_name %></a>
            <br/>
            <div class="metadata">
                <span class="date"><%= created_time %></span>
            </div>
            <div class="text" style="min-width:55px">
                <div class="ui pointing label large <% if(is_mine) { %> right <% } %>">
                    <p><%= content %></p>
                </div>
            </div>
        </div>
    </script>

这里并没有定义user的模板，因为目前对user只是做了简单的展现，即仅在顶部栏上加了一个用户名，通过: ``user_name`` 这个Dom节点的id添加数据。

到目前已经介绍了所有的基础数据：从model到collection，到用来显示数据的view，再到定义的页面模板template。每部分的数据都可以单独的从后台获取，并且渲染。好了，材料都准备好了就差什么了？当然是流程。不过还有一个东西得先说一下，这些数据被塞到页面之后到底长成什么样还不知道。因此得先来看下页面结构。

下面先来看看上面的那些数据最终要被填充到页面的什么部位，然后再来说流程的事。


14.4 页面结构
------------------------------------

这里还是从代码上说事，但是最终效果图已经在 `wechat <https://github.com/the5fire/wechat>`_ 的readme中贴出来了，你可以跳过去看看长相先。

欣赏完外表，来看看内部的骨架，这里只贴主要代码。

*顶部的固定栏:*

.. code:: html

    <!-- Top Bar  -->
    <div class="ui fixed transparent inverted main menu">
        <div class="container">
            <div class="title item">
                <b>We Chat</b> 在线聊天系统
            </div>

            <div class="right menu">
                <div class="title item">
                    Backbonejs交流群：308466740
                </div>
            </div>
            <div id="user_info" class="right menu hide">
                <div class="title item">
                    <i class="icon user"></i>
                    <label id="username">the5fire</lable>
                </div>
                <a class="popup icon github item" href="/logout" title="退出登录">
                    退出登录
                </a>
            </div>
        </div>
    </div>


*登陆注册的代码，纯静态代码:*

.. code:: html

    <div id="wrapper" style="display: block; z-index: 998;">
        <div class="container">
            <div id="login" class="ui two column relaxed grid">
                <div class="column">
                    <div class="ui fluid form segment">
                        <h3 class="ui header">登录</h3>
                        <div class="field">
                            <label>用户名</label>
                            <input id="login_username" placeholder="用户名" type="text">
                        </div>
                        <div class="field">
                            <label>密码</label>
                            <input id="login_pwd" type="password">
                        </div>
                        <div class="ui blue login_submit button">登录</div>
                    </div>
                </div>
                <div class="column">
                    <div class="ui fluid form segment">
                        <h3 class="ui header">注册</h3>
                        <div class="field">
                            <label>用户名</label>
                            <input id="reg_username" placeholder="用户名" type="text">
                        </div>
                        <div class="field">
                            <label>密码</label>
                            <input id="reg_pwd" type="password">
                        </div>
                        <div class="field">
                            <label>重复密码</label>
                            <input id="reg_pwd_repeat" type="password">
                        </div>
                        <div class="inline field">
                            <div class="ui checkbox">
                                <input type="checkbox" id="terms">
                                <label for="terms">我同意the5fire's WeChat网的服务条款。</label>
                            </div>
                        </div>
                        <div class="ui blue registe_submit button">注册</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

用来展示话题和消息的内容区域:

.. code:: html

    <!-- Content -->
    <div id="main" class="main container">

        <!-- Topic List -->
        <div id="topic_section">
            <div id="topic_list" class="ui three column grid">
                <!-- 这里放topic列表 -->
            </div>
            <div id="topic_form" class="ui error form segment">
                <div class="two fields">
                    <div class="field">
                        <label>新建Topic</label>
                        <input id="topic_title" placeholder="topic" type="text">
                    </div>
                </div>
                <div class="ui blue submit_topic button">Add</div>
            </div>
        </div>

        <!-- Message -->
        <div  id="message_section" class="ui column grid hide" style="display:none">
            <div class="column">
                <div class="circular ui button"><a href="#index">返回列表</a></div>
                <div class="ui piled blue segment">
                    <h2 class="ui header">
                        #<i id="message_head"></i># <!-- 用来放topic name -->
                    </h2>
                    <div id="message_list" class="ui comments">
                        <!-- comments 列表 -->
                    </div>
                    <div class="ui reply form">
                        <div class="field">
                            <input type="text" id="comment"/>
                        </div>
                        <div id="submit" data="" class="ui fluid blue labeled submit icon button">
                            <i class="icon edit"></i> 我也来说一句！
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

页面布局大概介绍了一下，如果你熟悉html，并且也看了我上面链接里给的最终效果， 上面的这些理解上面的这些代码应该很Easy了。如果不熟悉的也没问题，只要关注于我写了注释的地方就行了，这些地方就是上面我们定义的那些模板被渲染好之后的归宿。


14.5 view管理和router管理
-----------------------------------------------

上面占了点篇幅介绍了页面的布局，以便对我们数据最终的处理有一个感觉。

有了数据，也有了最后数据的去处，最后当然要说流程了。所谓的流程就是说我要怎么把Model渲染好的模板给塞到对于的页面div节点中，我要怎么来控制不同Model的展示。毕竟是SPA(单页应用), 也只有这一个页面来供数据的展示。因此需要在一个页面上切换的展示不同的视图。

这里我们是通过Backbone的Route和View来做。Route用来做路由分发（也就是URI的匹配，比如：#index匹配到首页）。另外不同于上面用来把Model数据传到Template中的View，这里的View是用来管理其他具体View和Collection的,可以比喻为管家View，就是用来控制这个视图什么时候显示，那个Collection的数据什么时候获取。

但是，需要注意，这个View需要被Route来控制，也就是通过路由控制（根据URI），因此View在具备上述功能的情况下也要提供接口（方法）给Route。

上面介绍了一堆，仿佛说不太清晰，没关系，Talk is cheap, Show you my code。

先来看View管家-AppView, 主要功能就是获取Topic和Message的数据到Collection中，调用Model对应的View把数据填到模板中，然后把最终拼好的数据放到上面介绍的页面对应div中。

.. code:: javascript

    var AppView = Backbone.View.extend({
        el: "#main",
        topic_list: $("#topic_list"),
        topic_section: $("#topic_section"),
        message_section: $("#message_section"),
        message_list: $("#message_list"),
        message_head: $("#message_head"),

        events: {
            'click .submit': 'saveMessage', // 发送消息
            'click .submit_topic': 'saveTopic',  // 新建主题
            'keypress #comment': 'saveMessageEvent', // 键盘事件
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
            // 获取所有主题
            topics.fetch();
            this.topic_section.show();
            this.message_section.hide();
            this.message_list.html('');
        },

        initMessage: function(topic_id) {
            // 初始化消息集合，并放到消息池中
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

上面是所有数据视图的展示的逻辑控制部分，虽然代码很多，但没有复杂逻辑，很直观。这里只是Topic和Message的展示。但是这些所有的数据都是需要用户登录之后才能看到的，那么用户登录和注册部分的逻辑在哪呢？在上面的页面布局部分已经展示了登录注册的页面，下面展示下具体逻辑。

登录注册-LoginView:

.. code:: javascript

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

这里的View的主要功能是：注册（保存user数据到后台），登录（发送用户请求到后台,成功则跳到首页)，事件监听和处理。很基础的功能。

从上面两部分我们知道了如何控制不同Model对应视图的展示，也知道了如何处理用户登录。下面再来看些Route部分是如何把url匹配到对应的方法上的。

路由部分代码-AppRouter:

.. code:: javascript

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

这里设定了三条路由：login，index，topic，分别对应这个登录视图（LoginView), 主题和Message的视图（由AppView管理）。

在不同的路由中的逻辑大致一样，就是根据当前的条件决定是否现实视图。 比如index中的 ``if (g_user && g_user.id != undefined) {`` 就是判断当前环境中是否有g_user这个对象（这个对象是用来存放已登录用户数据的，后面会介绍)，根据这个对象判断是否用户已经登录，进而决定是否现实首页——topic列表页。

14.6 启动
----------------------

当所有的逻辑都定义好之后，页面加载完毕首先要做的就是启动整个流程，怎么启动呢？按照我们的项目结构：AppRouter管理AppView和LoginView，AppView管理TopicView和MessageView，因此，只需要启动AppRouter即可。

启动代码如下:

.. code:: javascript

    var appRouter = new AppRouter();
    var g_user = new User();
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
 
就是这一小段代码，程序可以正常运行了。这段代码中的逻辑是：声明一个全局的appRouter和g_user，然后获取当前用户（服务器端会通过session保存对应浏览器的信息）， 之后根据获取到得用户状态做进一步操作（到登录页面或是到首页）。

这里需要注意的是，这段代码只有在页面加载（刷新或重新访问）的时候才会执行。

好了，到此为止整个项目已经介绍完毕了，不知道你是否看懂，或者这么问，我是否把这个项目讲明白了？

14.7 总结
------------------------------

这一篇看起篇幅很长，其实都是代码。而这些代码只有当你真正打算做这么个东西的时候才会主动去理解，因为那些走马观花的人会选择性的忽略代码。

最后还是补充一下整个流程，其实整个项目开始做的时候，项目的设计者就应该有一个具体的需求和用户使用的场景。对于这个项目我自己设想的用户使用流程：

用户打开浏览器，看到登录和注册页面——》输入用户名、密码进行登录（注册）操作——》展示主题列表视图，并显示用户名在顶部——》用户创建并进入某一主题（显示消息列表视图）——》用户发送消息，消息保存的同时获取服务器端的消息到当前视图。

另外一定要说的是，项目没有进行太多优化和代码的精简，还有很多改进的地方。在我写代码的这些年中我始终坚信并践行的一件事就是——获取知识最好的方法就是实践。因此如果你想掌握这个Backbone这个工具，最佳的方式是开始一个项目，并持续的做下去。或者参与一个项目，持续改善项目。

我在边写边实践中写了 `WeChat <https://github.com/the5fire/wechat>`_ 这个项目，并且已经部署上线，相信会是一个好的开始，因为我没打算把它仅仅作为一个Demo来用。 本文涉及的所有代码均在该项目的basic-version分支可以看到。



**导航**

* 上一章 13  `前后端实战演练：Web聊天室-后端开发 <13-web-chatroom-base-on-backbonejs-3.rst>`_
* 下一章 15  `引入requirejs <15-import-requirejs.rst>`_
