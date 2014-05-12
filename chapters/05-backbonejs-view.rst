第五章 Backbonejs中的View实践
=======================================================================

前面介绍了存放数据的Model和Collection以及对用户行为进行路由分发的Router（针对链接）。这一节终于可以往页面上放点东西来玩玩了。这节就介绍了Backbone中得View这个模块。Backbone的View是用来显示你的model中的数据到页面的，同时它也可用来监听DOM上的事件然后做出响应。但是这里要提一句的是，相比于Angularjs中model变化之后页面数据自动变化的特性，Backbone要手动来处理。至于这两种方式的对比，各有优劣，可以暂时不关心。

下面依然是通过几个示例来介绍下view的功能,首先给出页面的基本模板：

.. code:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>the5fire-backbone-view</title>
    </head>
    <body>
        <div id="search_container"></div>

        <script type="text/template" id="search_template">
            <label><%= search_label %></label>
            <input type="text" id="search_input" />
            <input type="button" id="search_button" value="Search" />
        </script>
    <script src="http://the5fireblog.b0.upaiyun.com/staticfile/jquery-1.10.2.js"></script>
    <script src="http://the5fireblog.b0.upaiyun.com/staticfile/underscore.js"></script>
    <script src="http://the5fireblog.b0.upaiyun.com/staticfile/backbone.js"></script>
    <script>
    (function ($) {
        //此处添加下面的试验代码
    })(jQuery);
    </script>
    </body>
    </html>

5.1 一个简单的view
--------------------------------------------

.. code:: javascript

    var SearchView = Backbone.View.extend({
        initialize: function(){ 
            alert('init a SearchView'); 
        } 
    }); 
    var searchView = new SearchView();

是不是觉得很没有技术含量，所有的模块定义都一样。


5.2 el属性
-------------------------------------

这个属性用来引用DOM中的某个元素，每一个Backbone的view都会有这么个属性，如果没有显示声明，Backbone会默认的构造一个，表示一个空的div元素。el标签可以在定义view的时候在属性中声明，也可以在实例化view的时候通过参数传递。

.. code:: javascript

    var SearchView = Backbone.View.extend({
        initialize: function(){
            alert('init a SearchView');
        }
    });

    var searchView = new SearchView({el: $("#search_container")});

这段代码简单的演示了在实例化的时候传递el属性给View。下面我们来看看模板的渲染。

.. code:: javascript

    var SearchView = Backbone.View.extend({
        initialize: function(){ 
        }, 
        render: function(context) {
            //使用underscore这个库，来编译模板
            var template = _.template($("#search_template").html(), context);
            //加载模板到对应的el属性中
            $(this.el).html(template);
        }
    });
    var searchView = new SearchView({el: $("#search_container")});
    searchView.render({search_label: "搜索渲染"});  //这个reander的方法可以放到view的构造函数中,这样初始化时就会自动渲染

运行页面之后，会发现script模板中的html代码已经添加到了我们定义的div中。

*这里面需要注意的是在模板中定义的所有变量必须在render的时候传递参数过去，不然就会报错。*
关于el还有一个东西叫做$el,这个东西是对view中元素的缓存。



5.3 再来看view中event的使用
--------------------------------------------------------------------------
页面上的操作除了可以由之前的router来处理之外，在一个view中定义元素，还以可以使用event来进行事件绑定。这里要注意的是在view中定义的dom元素是指你el标签所定义的那一部分dom节点，event进行事件绑定时会在该节点范围内查找。

来，继续看代码。

.. code:: javascript

    var SearchView = Backbone.View.extend({
        el: "#search_container",

        initialize: function(){
            this.render({search_label: "搜索按钮"});
        },
        render: function(context) {
            //使用underscore这个库，来编译模板
            var template = _.template($("#search_template").html(), context);
            //加载模板到对应的el属性中
            $(this.el).html(template);
        },

        events:{  //就是在这里绑定的
            'click input[type=button]' : 'doSearch'  //定义类型为button的input标签的点击事件，触发函数doSearch

        },

        doSearch: function(event){
            alert("search for " + $("#search_input").val());
        }

    });

    var searchView = new SearchView();

自己运行下，是不是比写$("input[type=button]").bind('click',function(){})好看多了。



5.4 View中的模板
----------------------------
上面已经简单的演示了模板的用法，如果你用过django模板的话，你会发现模板差不多都是那么回事。上面只是简单的单个变量的渲染，那么逻辑部分怎么处理呢，下面来看下。

把最开始定义的模板中的内容换成下面这个。

.. code:: html

    <ul>
    <% _.each(labels, function(name) { %> 
        <% if(name != "label2") {%>
        <li><%= name %></li> 
        <% } %>
    <% }); %>
    </ul>

下面是js代码

.. code:: javascript

    var SearchView = Backbone.View.extend({
        el: "#search_container",

        initialize: function(){
            var labels = ['label1', 'label2', 'label3'];
            this.render({labels: labels}); 
        },

        render: function(context) {
            //使用underscore这个库，来编译模板
            var template = _.template($("#search_template").html(), context);
            //加载模板到对应的el属性中
            $(this.el).html(template);
        },

    });

    var searchView = new SearchView();

再次运行，有木有觉得还不错，模板中使用的就基本的js语法。

总结一下，关于view中的东西就介绍这么多，文档上还有几个其他的属性，不过大体用法都一致。在以后的实践中用到在介绍。


**导航**

* 上一章 04 `Backbonejs中的Router实践 <04-backbonejs-router.rst>`_
* 下一章 06 `实战演练：todos分析（一） <06-backbonejs-todos-1.rst>`_
