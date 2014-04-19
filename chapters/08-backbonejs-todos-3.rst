第八章 实战演练：todos分析（三）总结
=======================================================================

在前两篇文章中，我们已经对这个todos的功能、数据模型以及各个模块的实现细节进行了分析，这篇文章我们要对前面的分析进行一个整合。

首先让我们来回顾一下我们分析的流程：1. 先对页面功能进行了分析；2. 然后又分析了数据模型；3. 最后又对view的功能和代码进行了详解。你是不是觉得这个分析里面少了点什么？没错，就知道经验丰富的你已经看出来了，这里面少了对于流程的分析。这篇文章就对整体流程进行分析。

所以从我的分析中可以看的出来，我是先对各个原材料进行分析，然后再整体的分析（当然前提是我是理解流程的），这并不是分析代码的唯一方法，有时我也会采用跟着流程分析代码的方法。当然还有很多其他的分析方法，大家都有自己的套路嘛。

下面简单的说说流程分析的方法。记得多年前在学vb的时候，分析一个完整项目代码的时候，习惯从程序的入口点开始分析。虽然web网站和桌面软件的实现不同，但是大致思路是一样的（同时也有网站即软件的说法，在RESTful架构中）。所以我们要先找到网站的入口点所在。

和桌面应用项目的分析一样，网站的入口点就在于网页加载的时候。对于todos，自然就是在页面加载完之后执行的操作了，然后就看到下面的代码。

首先是对AppView的一个实例化：

.. code:: javascript

    var App = new AppView;


实例化，自然就会调用构造函数：

.. code:: javascript

    //在初始化过程中，绑定事件到Todos上，
    //当任务列表改变时会触发对应的事件。
    //最后从localStorage中fetch数据到Todos中。
    initialize: function() {
        this.input = this.$("#new-todo");
        this.allCheckbox = this.$("#toggle-all")[0];

        this.listenTo(Todos, 'add', this.addOne);
        this.listenTo(Todos, 'reset', this.addAll);
        this.listenTo(Todos, 'all', this.render);

        this.footer = this.$('footer');
        this.main = $('#main');

        Todos.fetch();
    },

注意其中的Todos.fetch()方法，前面说过，这个项目是在客户端保存数据，所以使用fetch方法并不会发送请求到服务器。另外在前面关于collection的单独讲解中我们也介绍了fetch执行完成之后，会调用set（默认）或者reset（需要手动设置 ``{reset: true}`` ）。所以在没有指明fetch的reset参数的情况下，backbonejs的Collection中的set方法会遍历Todos的内容并且调用add方法。

在initialize中我们绑定了add到addOne上，因此在fetch的时候会Backbonejs会帮我们调用addOne（其实也是在collection的set方法中）。和collection中的set类似的，我们可以自定义reset方法，自行来处理fetch到得数据，但是需要在fetch时手动添加reset参数。

PS: 感谢网友指正

这里先来看下我们绑定到reset上的addAll方法是如何处理fetch过来的数据的:

.. code:: javascript

    // 添加一个任务到页面id为todo-list的div/ul中
    addOne: function(todo) {
        var view = new TodoView({model: todo});
        this.$("#todo-list").append(view.render().el);
    },

    // 把Todos中的所有数据渲染到页面,页面加载的时候用到
    addAll: function() {
        Todos.each(this.addOne, this);
    },

在addAll中调用addOne方法，关于Todos.each很好理解，就是语法糖（简化的for循环）。关于addOne方法的细节下面介绍。

然后再来看添加任务的流程，一个良好的代码命名风格始终是让人满心欢喜的。因此很显然，添加一个任务，自然就是addOne,其实你看events中的绑定也能知道，先看一下绑定：

.. code:: javascript

    // 绑定dom节点上的事件
    events: {
        "keypress #new-todo":  "createOnEnter",
        "click #clear-completed": "clearCompleted",
        "click #toggle-all": "toggleAllComplete"
    },

这里并没有addOne方法的绑定，但是却有createOnEnter，语意其实一样的。来看主线，createOnEnter这个方法：

.. code:: javascript

    //创建一个任务的方法，使用backbone.collection的create方法。将数据保存到localStorage,这是一个html5的js库。需要浏览器支持html5才能用。
    createOnEnter: function(e) {
        if (e.keyCode != 13) return;
        if (!this.input.val()) return;

        //创建一个对象之后会在backbone中动态调用Todos的add方法，该方法已绑定addOne。
        Todos.create({title: this.input.val()});
        this.input.val('');
    },

注释已写明，Todos.create会调用addOne这个方法。由此顺理成章的来到addOne里面：

.. code:: javascript

    //添加一个任务到页面id为todo-list的div/ul中
    addOne: function(todo) {
        var view = new TodoView({model: todo});
        this.$("#todo-list").append(view.render().el);
    },

在里面实例化了一个TodoView类，前面我们说过，这个类是主管各个任务的显示的。具体代码就不细说了。

有了添加再来看更新，关于单个任务的操作，我们直接找TodoView就ok了。所以直接找到

.. code:: javascript

    // 为每一个任务条目绑定事件
    events: {
        "click .toggle"   : "toggleDone",
        "dblclick .view"  : "edit",
        "click a.destroy" : "clear",
        "keypress .edit"  : "updateOnEnter",
        "blur .edit"      : "close"
    },

其中的edit事件的绑定就是更新的一个开头，而updateOnEnter就是更新的具体动作。所以只要搞清楚这俩方法的作用一切就明了了。这里同样不用细说。

在往后还有删除一条记录以及清楚已有记录的功能，根据上面的分析过程，我想大家都很容易的去‘顺藤模瓜’。

关于Todos的分析到此就算完成了。

在下一篇文章中我们将一起来学习通过web.py来搭建web服务器，以及简单的数据库的使用。


**导航**

* 上一章 07 `实战演练：todos分析（二）view的应用 <07-backbonejs-todos-2.rst>`_
* 下一章 09  `后端环境搭建：web.py的使用 <09-intro-webpy.rst>`_
