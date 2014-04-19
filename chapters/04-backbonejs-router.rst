第四章 Backbonejs中的Router实践
=======================================================================

前面介绍了Model和Collection，基本上属于程序中静态的数据部分。这一节介绍Backbone中的router，属于动态的部分，见名之意，router——路由的意思，显然是能够控制url指向哪个函数的。具体是怎么做的一会通过几个实例来看看。

在现在的单页应用中，所有的操作、内容都在一个页面上呈现，这意味着浏览器的url始终要定位到当前页面。那么一个页面中的左右的操作总不能都通过事件监听来完成，尤其是对于需要切换页面的场景以及需要分享、收藏固定链接的情况。因此就有了router，通过hash的方式（即#page）来完成。不过随着浏览器发展，大多数的浏览器已经可以通过history api来操控url的改变，可以直接使用 /page 来完成之前需要hash来完成的操作，这种方式看起来更为直观一些。下面提供过几个demo来切实体会一番。

4.1 一个简单的例子
--------------------------------------------

.. code:: javascript

    var AppRouter = Backbone.Router.extend({
        routes: {
            "*actions" : "defaultRoute"
        },

        defaultRoute : function(actions){
            alert(actions);
        }
    });

    var app_router = new AppRouter;

    Backbone.history.start();


需要通过调用Backbone.history.start()方法来初始化这个Router。

在页面上需要有这样的a标签：

::

    <a href="#actions">testActions</a>

点击该链接时，便会触发defaultRouter这个方法。


4.2 这个routes映射要怎么传参数
-----------------------------------------------------------

看下面例子，立马你就知道了

.. code:: javascript

    var AppRouter = Backbone.Router.extend({

        routes: {
            "posts/:id" : "getPost",
            "*actions" : "defaultRoute"
        },

        getPost: function(id) {
            alert(id);
        },

        defaultRoute : function(actions){
            alert(actions);
        }
    });

    var app_router = new AppRouter;
    Backbone.history.start();

对应的页面上应该有一个超链接：

::

    <a href="#/posts/120">Post 120</a>

从上面已经可以看到匹配#标签之后内容的方法，有两种：一种是用“:”来把#后面的对应的位置作为参数；还有一种是“*”，它可以匹配所有的url，下面再来演练一下。

.. code:: javascript

    var AppRouter = Backbone.Router.extend({

        routes: {
            "/posts/:id" : "getPost",
            //下面对应的链接为<a href="#/download/user/images/hey.gif">download gif</a>
            "/download/*path": "downloadFile",
            //下面对应的链接为<a href="#/dashboard/graph">Load Route/Action View</a>
            "/:route/:action": "loadView",
            "*actions" : "defaultRoute"
        },

        getPost: function(id) {
            alert(id);
        },

        defaultRoute : function(actions){
            alert(actions);
        },

        downloadFile: function( path ){ 
            alert(path); // user/images/hey.gif 
        },

        loadView: function( route, action ){ 
            alert(route + "_" + action); // dashboard_graph 
        }

    });

    var app_router = new AppRouter;
    Backbone.history.start();

4.3 手动触发router
----------------------------------
上面的例子都是通过页面点击触发router到对应的方法上，在实际的使用中，还存在一种场景就是需要在某一个逻辑中触发某一个事件，就像是jQuery中得trigger一样，下面的代码展示怎么手动触发router。

.. code:: javascript

    routes: {
        "posts/:id" : "getPost",
        "manual": "manual",
        "*actions": "defaultRoute",
    },
    // 省略部分代码
    loadView: function( route, action ){ 
        alert(route + "_" + action); // dashboard_graph 
    },
    manual: function() {
        alert("call manual");
        app_router.navigate("/posts/" + 404, {trigger: true, replace: true});
    }

对应着在页面添加一个a标签： ``<a href="#/manual">manual</a>`` 然后点击这个链接，便会触发posts/:id对应的方法。

这里需要解释的是navigate后面的两个参数。trigger表示触发事件，如果为false，则只是url变化，并不会触发事件，replace表示url替换，而不是前进到这个url，意味着启用该参数，浏览器的history不会记录这个变动。

完整代码依然在 ``code`` 中可以找到。


**导航**

* 上一章 03  `Backbonejs中的Collections实践 <03-backbonejs-collection.rst>`_
* 下一章 05 `Backbonejs中的View实践 <05-backbonejs-view.rst>`_
