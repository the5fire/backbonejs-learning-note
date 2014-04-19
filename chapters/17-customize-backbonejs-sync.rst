第十七章 定制Backbonejs
=========================================

这里说的定制Backbonejs，主要是定制Backbone中的sync部分，也就是最后和服务器端通信的部分。

17.1 三个级别的定制
-------------------------------------

首先得说，在Backbone里面和后端能通信的对象也就两个——Model和Collection。这俩的主要工作就是从服务器拉取数据，保存到实例中，或者把实例中的属性发送到服务器端。

上面两中类型的对象都是基于Backbone.sync来进行通信的，同时也可以定义各自的sync方法，类似这样：

*Model级别的*

.. code:: javascript

    var Message = Backbone.Model.extend({
        urlRoot: '/message',
        # 这么写, 打印要操作的实体, 调用系统的sync
        sync: function(method, model, options){
            console.log(model);
            return Backbone.sync(method, model, options);
        },
    });

*Collection级别的*

.. code:: javascript

    var Messages = Backbone.Collection.extend({
        url: '/message',
        model: Message,
        # 这么写, 打印要操作的实体, 调用系统的sync
        sync: function(method, collection, options){
            console.log(collection);
            return Backbone.sync(method, collection, options);
        },
    });

当然，也会存在这样的需求，要修改全局的sync：

.. code:: javascript

    var old_sync = Backbone.sync;
    Backbone.sync = function(method, model, options) {
        console.log(model);
        return old_sync(method, model, options);
    }

所谓定制，是Backbonejs给开发者提供的可以被重写的接口。因此定制过程也得符合Backbone对sync的定义。

17.2 简单实例，用socketio通信
---------------------------------------------------------

在 `wechat <https://github.com/the5fire/wechat>`_ 这个项目中为了保证聊天的实时性，我引入了socketio，后端使用gevent-socketio，（socketio这个东西不打算写，和主题关系不大，有需求的可以题issue）。

实时聊天的需求主要是在Message上，用户A发送一个请求，在同一聊天室内的其他用户应该立马能看见。之前有两个版本：

* 第一版是发送message时会调用messages的fetch方法，也就是用户只有发言才能看到别人发的聊天内容，代码如下：

.. code:: javascript

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

* 第二版是引入socketio之后，在save完数据之后，通过socket把数据再次发送到服务器上的socket端，服务器再挨个发送数据到各个客户端，代码如下：

.. code:: javascript

    message.save(null, {
        success: function(model, response, options){
            comment_box.val('');
            messages.add(response);
            // 发送成功之后，通过socket再次发送
            // FIXME: 最后可通过socket直接通信并保存
            socket.emit('message', response);
        },
    });

    // 对应着有一个socket监听, 监听服务器发来的消息
    // 监听message事件，添加对话到messages中
    socket.on('message', function(response) {
        messages.add(response);
    });

可以看得出来，上面的第二版算是比较合适了，但是还是有些别扭，数据要重复发送。因此终于到了需要定制的时刻了。

上面说了，有三种级别的定制。根据我的需求，只需要定制Model级别的就可以了，怎么定制呢？

和一开头的示例代码类似：

.. code:: javascript

    var Message = Backbone.Model.extend({
        urlRoot: '/message',

        sync: function(method, model, options){
            if (method === 'create') {
                socket.emit('message', model.attributes);
                $('#comment').val('');
            } else {
                return Backbone.sync(method, model, options);
            };
        },
    });

    // 对应着上面的那个message.save后的一堆东西都可以去掉了，直接
    message.save();

这样就好了，客户端只需要发送一次数据。但要记得在服务器端的监听message的接口上添加保存message的逻辑。

好了，定制就介绍这么多。关于上面提到的代码想了解上下文的，可以到我的wechat这个项目的master分支查看。


**导航**

* 上一章 16  `补充异常处理 <16-exception-in-backbone.rst>`_
* 下一章 18  `再次总结的说 <18-backbone-summary.rst>`_
