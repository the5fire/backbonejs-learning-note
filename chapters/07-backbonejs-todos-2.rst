第七章 实战演练：todos分析（二）View的应用
=======================================================================

在上一篇文章中我们把todos这个实例的数据模型进行了简单的分析，有关于数据模型的操作也都知道了。接着我们来看剩下的两个view的模型，以及它们对页面的操作。

7.1 为什么要两个view
------------------------------
首先要分析下，这俩view是用来干嘛的。有人可能会问了，这里不就是一个页面吗？一个view掌控全局不就完了？

我觉得这就是新手和老手的主要区别之一，喜欢在一个方法里面搞定一切，喜欢把东西都拧到一块去，觉得这样看起来容易。熟不知，这样的代码对于日后的扩展会造成很大的麻烦。因此我们需要学习下优秀的设计，从好的代码中汲取营养。

这里面的精华就是，将对数据的操作和对页面的操作进行分离，也就是现在代码里面TodoView和AppView。前者的作用是对把Model中的数据渲染到模板中;后者是对已经渲染好的数据进行处理。两者各有分工，TodoView可以看做是加工后的数据，这个数据就是待使用的html数据。

7.2 TodoView的代码分析
-------------------------
TodoView是和Model一对一的关系，在页面上一个View也就展示为一个item。除此之外，每个view上还有其他的功能，比如编辑模式，展示模式，还有对用户的输入的监听。详细还是来看下代码：

.. code:: javascript

    // 首先是创建一个全局的Todo的collection对象

    var Todos = new TodoList;

    // 先来看TodoView，作用是控制任务列表
    var TodoView = Backbone.View.extend({

        //下面这个标签的作用是，把template模板中获取到的html代码放到这标签中。
        tagName:  "li",

        // 获取一个任务条目的模板,缓存到这个属性上。
        template: _.template($('#item-template').html()),

        // 为每一个任务条目绑定事件
        events: {
            "click .toggle"   : "toggleDone",
            "dblclick .view"  : "edit",
            "click a.destroy" : "clear",
            "keypress .edit"  : "updateOnEnter",
            "blur .edit"      : "close"
        },

        //在初始化时设置对model的change事件的监听
        //设置对model的destroy的监听，保证页面数据和model数据一致
        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
            //这个remove是view的中的方法，用来清除页面中的dom
            this.listenTo(this.model, 'destroy', this.remove);
        },

        // 渲染todo中的数据到 item-template 中，然后返回对自己的引用this
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            this.$el.toggleClass('done', this.model.get('done'));
            this.input = this.$('.edit');
            return this;
        },

        // 控制任务完成或者未完成
        toggleDone: function() {
            this.model.toggle();
        },

        // 修改任务条目的样式
        edit: function() {
            $(this.el).addClass("editing");
            this.input.focus();
        },

        // 关闭编辑模式，并把修改内容同步到Model和界面
        close: function() {
            var value = this.input.val();
            if (!value) { //无值内容直接从页面清除
                this.clear();
            } else {
                this.model.save({title: value});
                this.$el.removeClass("editing");
            }
        },

        // 按下回车之后，关闭编辑模式
        updateOnEnter: function(e) {
          if (e.keyCode == 13) this.close();
        },

        // 移除对应条目，以及对应的数据对象
        clear: function() {
            this.model.destroy();
        }
    });

7.3 AppView的代码分析
--------------------------------
再来看AppView，功能是显示所有任务列表，显示整体的列表状态（如：完成多少，未完成多少）

.. code:: javascript

    //以及任务的添加。主要是整体上的一个控制
    var AppView = Backbone.View.extend({

        //绑定页面上主要的DOM节点
        el: $("#todoapp"),

        // 在底部显示的统计数据模板
        statsTemplate: _.template($('#stats-template').html()),

        // 绑定dom节点上的事件
        events: {
            "keypress #new-todo":  "createOnEnter",
            "click #clear-completed": "clearCompleted",
            "click #toggle-all": "toggleAllComplete"
        },

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

        // 更改当前任务列表的状态
        render: function() {
            var done = Todos.done().length;
            var remaining = Todos.remaining().length;

            if (Todos.length) {
                this.main.show();
                this.footer.show();
                this.footer.html(this.statsTemplate({done: done, remaining: remaining}));
            } else {
                this.main.hide();
                this.footer.hide();
            }

            //根据剩余多少未完成确定标记全部完成的checkbox的显示
            this.allCheckbox.checked = !remaining;
        },

        // 添加一个任务到页面id为todo-list的div/ul中
        addOne: function(todo) {
            var view = new TodoView({model: todo});
            this.$("#todo-list").append(view.render().el);
        },

        // 把Todos中的所有数据渲染到页面,页面加载的时候用到
        addAll: function() {
            Todos.each(this.addOne, this);
        },

        //生成一个新Todo的所有属性的字典
        newAttributes: function() {
            return {
                content: this.input.val(),
                order:   Todos.nextOrder(),
                done:    false
            };
        },

        //创建一个任务的方法，使用backbone.collection的create方法。将数据保存到localStorage,这是一个html5的js库。需要浏览器支持html5才能用。
        createOnEnter: function(e) {
            if (e.keyCode != 13) return;
            if (!this.input.val()) return;

            //创建一个对象之后会在backbone中动态调用Todos的add方法，该方法已绑定addOne。
            Todos.create({title: this.input.val()});
            this.input.val('');
        },

        //去掉所有已经完成的任务
        clearCompleted: function() {
            // 调用underscore.js中的invoke方法，对过滤出来的todos调用destroy方法
            _.invoke(Todos.done(), 'destroy');
            return false;
        },

        //处理页面点击标记全部完成按钮
        //处理逻辑：如果标记全部按钮已选，则所有都完成，如果未选，则所有的都未完成。
        toggleAllComplete: function () {
            var done = this.allCheckbox.checked;
            Todos.each(function (todo) { todo.save({'done': done}); });
        }
    });

通过上面的代码，以及其中的注释，我们认识里面每个方法的作用。下面来看最重要的，页面部分。

7.4 页面模板分析
-----------------------
在前几篇的view介绍中我们已经认识过了简单的模板使用，以及变量参数的传递，如：

.. code:: html

    <script type="text/template" id="search_template">

            <label><%= search_label %></label>
            <input type="text" id="search_input" />
            <input type="button" id="search_button" value="Search" />

    </script>


既然能定义变量，那么就能使用语法，如同django模板，那来看下带有语法的模板，也是上面的两个view用到的模板，我想这个是很好理解的。

.. code:: html

    <script type="text/template" id="item-template">
        <div class="view">
            <input class="toggle" type="checkbox" <%= done ? 'checked="checked"' : '' %> />
            <label><%- title %></label>
            <a class="destroy"></a>
        </div>
        <input class="edit" type="text" value="<%- title %>" />
    </script>


    <script type="text/template" id="stats-template">
        <% if (done) { %>
            <a id="clear-completed">Clear <%= done %> completed <%= done == 1 ? 'item' : 'items' %></a>
        <% } %>
        <div class="todo-count"><b><%= remaining %></b> <%= remaining == 1 ? 'item' : 'items' %> left</div>
    </script>

简单的语法，上面的那个对应TodoView。有木有觉得比之前的那一版简洁太多了，有木有！！啥叫代码的美感，对比一下就知道了。

这一篇文章就先到此为止，文章中我们了解到在todos这个实例中，view的使用，以及具体的TodoView和AppView中各个函数的作用，这意味着所有的肉和菜都已经放到你碗里了，下面就是如何吃下去的问题了。

下一篇我们一起来学习todos的整个流程。


**导航**

* 上一章 06 `实战演练：todos分析（一） <06-backbonejs-todos-1.rst>`_
* 下一章 08 `实战演练：todos分析（三）总结 <08-backbonejs-todos-3.rst>`_
