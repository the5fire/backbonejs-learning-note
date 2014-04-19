第一章 Hello Backbonejs
=======================================================================

1.1 基础概念
--------------------
Backbone，英文意思是：勇气， 脊骨，但是在程序里面，尤其是在Backbone后面加上后缀js之后，它就变成了一个框架，一个js库。

Backbone.js，不知道作者是以什么样的目的来对其命名的，可能是希望这个库会成为web端开发中脊梁骨。 

好了，八卦完了开始正题。

Backbone.js提供了一套web开发的框架，通过Models进行key-value绑定及自定义事件处理，通过Collections提供一套丰富的API用于枚举功能，通过Views来进行事件处理及与现有的Application通过RESTful JSON接口进行交互.它是基于jQuery和underscore的一个前端js框架。

整体上来说，Backbone.js是一个web端javascript的MVC框架，算是轻量级的框架。它能让你像写Java（后端）代码组织js代码，定义类，类的属性以及方法。更重要的是它能够优雅的把原本无逻辑的javascript代码进行组织，并且提供数据和逻辑相互分离的方法，减少代码开发过程中的数据和逻辑混乱。

在Backbonejs有几个重要的概念，先介绍一下:Model，Collection，View，Router。其中Model是根据现实数据建立的抽象，比如人（People）；Collection是Model的一个集合，比如一群人；View是对Model和Collection中数据的展示，把数据渲染（Render）到页面上；Router是对路由的处理，就像传统网站通过url现实不同的页面，在单页面应用（SPA）中通过Router来控制前面说的View的展示。

通过Backbone，你可以把你的数据当作Models，通过Models你可以创建数据，进行数据验证，销毁或者保存到服务器上。当界面上的操作引起model中属性的变化时，model会触发change的事件。那些用来显示model状态的views会接受到model触发change的消息，进而发出对应的响应，并且重新渲染新的数据到界面。在一个完整的Backbone应用中，你不需要写那些胶水代码来从DOM中通过特殊的id来获取节点，或者手工的更新HTML页面，因为在model发生变化时，views会很简单的进行自我更新。

上面是一个简单的介绍，关于backbone我看完他的介绍和简单的教程之后，第一印象是它为前端开发制定了一套自己的规则，在这个规则下，我们可以像使用django组织python代码一样的组织js代码，它很优雅，能够使前端和server的交互变得简单。

在查backbone资料的时候，发现没有很系统的中文入门资料和更多的实例，所以我打算自己边学边实践边写，争取能让大家通过一系列文章能快速的用上Backbone.js。

关于backbone的更多介绍参看这个：

http://documentcloud.github.com/backbone/

http://backbonetutorials.com/


1.2 backbone的应用范围：
------------------------------

它虽然是轻量级框架，但是框架这东西也不是随便什么地方都能用的，不然就会出现杀鸡用牛刀，费力不讨好的结果。那么适用在哪些地方呢？

根据我的理解，以及Backbone的功能，如果单个网页上有非常复杂的业务逻辑，那么用它很合适，它可以很容易的操作DOM和组织js代码。

豆瓣的阿尔法城是一个极好的例子——纯单页、复杂的前端逻辑。

当然，除了我自己分析的应用范围之外，在Backbone的文档上看到了很多使用它的外国站点，有很多，说明Backbonejs还是很易用的。 

稍稍列一下国内用到Backbonejs的站点：

*1. 豆瓣阿尔法城*
链接：http://alphatown.com/

*2. 豆瓣阅读*
链接：http://read.douban.com/  主要用在图书的正文页

*3. 百度开发者中心*
链接：http://developer.baidu.com/

*4. 手机搜狐直播间*
链接：http://zhibo.m.sohu.com/

*5. OATOS企业网盘*
链接：http://app.oatos.com


1.3 学以致用
-----------------
现在，我们就要开始学习Backbonejs了，我假设你没有看过我的第一版，那一版有很多很多问题，在博客上也有很多人反馈。但是如果你把那一版看明白了，这新版的教程你可以粗略的浏览一遍，不过后面新补充的实践是要自己写出来、跑起来的。

先说我们为什么要学习这新的东西呢？简单说来是为了掌握更加先进的工具。那为什么要掌握先进的工具呢？简单来说就是为了让我们能够以更合理、优雅的方式完成工作，反应到代码上就是让代码变得可维护，易扩展。如果从复杂的方向来说的话，这俩话题都够我写好几天的博客了。

学以致用，最直接有效的就是用起来，光学是没用的，尤其是编程这样的实践科学。新手最常犯的一个错误就是喜欢不停的去看书，看过了就以为会了，然后就开始疯狂的学下一本。殊不知看懂和写出来能运行是两种完全不同的状态。因此建议新手——编程新手还是踏踏实实的把代码都敲了，执行了，成功了才是。

下面直接给一个简单的Demo出来，用到了Backbonejs的三个主要模块：Views，Collection，Model。通过执行这个例子，了解这个例子的运行过程，快速对要做的东西有一个感觉，然后再逐步击破。


1.4 完整DEMO
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
    
这里面涉及到backbone的三个部分，View、Model、Collection，其中Model代表一个数据模型，Collection是模型的一个集合，而View是用来处理页面以及简单的页面逻辑的。

动手把代码放到你的编辑器中吧，成功执行，然后修改某个地方，再次尝试。


**导航**

* 上一章 `00 前言 <00-preface.rst>`_
* 下一章 `02 Backbone中Model实践 <02-backbonejs-model.rst>`_
