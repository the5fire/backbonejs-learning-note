第六章 实战演练：todos分析（一）
=======================================================================

经过前面的几篇文章，Backbone中的Model, Collection，Router，View，都简单的介绍了一下，我觉得看完这几篇文章，差不多就能开始使用Backbone来做东西了，所有的项目无外乎对这几个模块的使用。不过对于实际项目经验少些的同学，要拿起来用估计会有些麻烦。因此这里就先找个现成的案例分析一下。

6.1 大家都来分析todos
------------------------------
关于Backbonejs实例分析的文章网上真是一搜一大把，之所以这么多，第一是这东西需求简单，不用花时间到理解情景中；第二是代码就是官方的案例，顺手可得，也省得去找了，自己琢磨一个不得花时间吗。

于是就有人问了，丫们都在分析todos，能不能有点新意呢。这问题要我说，如果你真的能把todos搞明白了，那其他的也就不用去看了。不管是看谁的分析，把这个搞明白的。所有的项目大体思路都差不多。尤其是对于这样的MVC的模型，就是往对应的模块里填东西。因此，不管有多少人都在分析这玩意，自己弄懂了才是应该关心的。

话虽如此，不同于网络上的绝大部分的分析的是，the5fire除了分析这个，还是对其进行了扩充，另外在后面也会有真实的案例。但我也是从这些案例的代码中汲取的营养。

补充一下，新版的todos代码相较于之前简直清晰太多，完全可以当做一个前端的范本来学习、模仿。


6.2 获取代码
--------------------
todos的代码这里下载：https://github.com/jashkenas/backbone/ ，建议自己clone一份到本本地。线上的地址是：http://backbonejs.org/examples/todos/index.html

clone下来之后可以在example中找到todos文件夹，文件结构如下：::

    examples
    ├── backbone.localStorage.js
    └── todos
        ├── destroy.png
        ├── index.html
        ├── todos.css
        └── todos.js

    1 directory, 5 files 

用浏览器打开index.html文件，推荐使用chome浏览器，就可以看到和官网一样的界面了。关键代码都在todos.js这个文件里。

6.3 功能分析
----------------------
首先来分析下页面上有哪些功能:

.. image:: http://the5fireblog.b0.upaiyun.com/staticfile/todos.png

从这个界面我们可以总结出来,下面这些功能::

    * 任务管理
        添加任务
        修改任务
        删除任务
    * 统计
        任务总计
        已完成数目

总体上就这几个功能。

这个项目仅仅是在web端运行的，没有服务器进行支持，因此在项目中使用了一个叫做backbone-localstorage的js库，用来把数据存储到前端。

6.4 从模型下手
------------------------
因为Backbone为MVC模式，根据对这种模式的使用经验，我们从模型开始分析。首先我们来看Model部分的代码:

.. code:: javascript

    /**
    *基本的Todo模型，属性为：content,order,done。
    **/
    var Todo = Backbone.Model.extend({
        // 设置默认的属性
        defaults: {
            title: "empty todo...",
            order: Todos.nextOrder(),
            done: false
        },

        // 设置任务完成状态
        toggle: function() {
            this.save({done: !this.get("done")});
        }
    });

这段代码是很好理解的，不过我依然是画蛇添足的加上了一些注释。这个Todo显然就是对应页面上的每一个任务条目。那么显然应该有一个collection来统治（管理）所有的任务，所以再来看collection：

.. code:: javascript

    /**
    *Todo的一个集合，数据通过localStorage存储在本地。
    **/

    var TodoList = Backbone.Collection.extend({

        // 设置Collection的模型为Todo
        model: Todo,
        //存储到浏览器，以todos-backbone命名的空间中
        localStorage: new Backbone.LocalStorage("todos-backbone"),

        //获取所有已经完成的任务数组
        done: function() {
            return this.where({done: true});
        },

        //获取任务列表中未完成的任务数组
        //这里的where在之前是没有的，但是语法上更清晰了
        //参考文档：http://backbonejs.org/#Collection-where
        remaining: function() {
            return this.where({done: false});
        },

        //获得下一个任务的排序序号，通过数据库中的记录数加1实现。
        nextOrder: function() {
            if (!this.length) return 1;

            return this.last().get('order') + 1;  // last获取collection中最后一个元素
        },

        //Backbone内置属性，指明collection的排序规则。
        comparator: 'order'
    });

collection的主要功能有以下几个：::

    1、按序存放Todo对象;
    2、获取完成的任务数目;
    3、获取未完成的任务数目;
    4、获取下一个要插入数据的序号。

如果你看过第一版的话，这里Backbone新的属性和方法(comparator和where)用起来更加符合语义了。

这篇文章先分析到这里，下篇文章继续分析。


**导航**

* 上一章 05 `Backbonejs中的View实践 <05-backbonejs-view.rst>`_
* 下一章 07 `实战演练：todos分析（二）View的应用 <07-backbonejs-todos-2.rst>`_
