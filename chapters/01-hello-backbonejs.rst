学以致用
-----------------
现在，我们就要开始学习Backbonejs了，我假设你没有看过我的第一版，那一版有很多很多问题，在博客上也有很多人反馈。但是如果你把那一版看明白了，这新版的教程你可以粗略的浏览一遍，不过后面新补充的实践是要自己写出来、跑起来的。

先说我们为什么要学习这新的东西呢？简单说来是为了掌握更加先进的工具。那为什么要掌握先进的工具呢？简单来说就是为了让我们能够以更合理、优雅的方式完成工作，反应到代码上就是让代码变得可维护，易扩展。如果从复杂的方向来说的话，这俩话题都够我写好几天的博客了。

学以致用，最直接有效的就是用起来，光学是没用的，尤其是编程这样的实践科学。新手最常犯的一个错误就是喜欢不停的去看书，看过了就以为会了，然后就开始疯狂的学下一本。殊不知看懂和写出来能运行是两种完全不同的状态。因此建议新手——编程新手还是踏踏实实的把代码都敲了，执行了，成功了才是。

下面直接给一个简单的Demo出来，用到了backbonejs的三个主要模块：Views，Collection，Model。通过执行这个例子，了解这个例子的运行过程，快速对要做的东西有一个感觉，然后再逐步击破。


完整DEMO
----------------
这个demo的主要功能是点击页面上得“新手报到”按钮，弹出对话框，输入内容之后，把内容拼上固定的字符串显示到页面上。事件触发的逻辑是： click 触发checkIn方法，然后checkIn构造World对象放到已经初始化worlds这个collection中。

来看完整的代码:

.. code:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>the5fire.com-backbone.js-Hello World</title>
    </head>
    <body>
        <button id="check">新手报到</button>
        <ul id="world-list">
        </ul>
        <a href="http://www.the5fire.com">更多教程</a>
        <script src="http://the5fireblog.b0.upaiyun.com/staticfile/jquery-1.10.2.js"></script>
        <script src="http://the5fireblog.b0.upaiyun.com/staticfile/underscore.js"></script>
        <script src="http://the5fireblog.b0.upaiyun.com/staticfile/backbone.js"></script>
        <script>
        (function ($) {
                World = Backbone.Model.extend({
                        //创建一个World的对象，拥有name属性
                        name: null
                });

                Worlds = Backbone.Collection.extend({
                        //World对象的集合
                        initialize: function (models, options) {
                                this.bind("add", options.view.addOneWorld);
                        }
                });

                AppView = Backbone.View.extend({
                        el: $("body"),
                        initialize: function () {
                                //构造函数，实例化一个World集合类，并且以字典方式传入AppView的对象
                                this.worlds = new Worlds(null, { view : this })
                        },
                        events: {
                                "click #check":  "checkIn",   //事件绑定，绑定Dom中id为check的元素
                        },
                        checkIn: function () {
                                var world_name = prompt("请问，您是哪星人?");
                                if(world_name == "") world_name = '未知';
                                var world = new World({ name: world_name });
                                this.worlds.add(world);
                        },
                        addOneWorld: function(model) {
                                $("#world-list").append("<li>这里是来自 <b>" + model.get('name') + "</b> 星球的问候：hello world！</li>");
                        }
                });
                //实例化AppView
                var appview = new AppView;
        })(jQuery);
        </script>
    </body>
    </html>
    
这里面涉及到backbone的三个部分，view、model、collection，其中model代表一个数据模型，collection是模型的一个集合，而view是用来处理页面以及简单的页面逻辑的。

动手把代码放到你的编辑器中吧，成功执行，然后修改某个地方，再次尝试。


**导航**

* 上一章 `00 前言 <00-preface.rst>`_
* 下一章 `02 Backbone中Model实践 <02-backbonejs-model.rst>`_
