第二章 Backbonejs中的Model实践
=======================================================================

上一章主要是通过简单的代码对Backbonejs做了一个概括的展示，这一章开始从Model层说起，详细解释Backbonejs中的Model这个东西。

对于Model这一部分，其官网是这么说的：“Model是js应用的核心，包括基础的数据以及围绕着这些数据的逻辑：数据转换、验证、属性计算和访问控制”。这句话基本上高度概括了Model在一个项目中的作用。实际上，不仅仅是js应用，在任何以数据收集和处理的项目中Model都是很重要的一块内容。

Model这个概念在我的印象中是来自于MVC这个东西，Model在其中的作用，除了是对业务中实体对象的抽象，另外的作用就是做持久化，所谓持久化就是把数据存储到磁盘上——文件形式、数据库形式。在web端也有对应的操作，比如存入LocalStorage，或者Cookie。

在web端，Model还有一个重要的功能就是和服务器端进行数据交互，就像是服务器端的程序需要和数据库交互一样。因此Model应该是携带数据流窜于各个模块之间的东西。

下面让我们通过一个一个的实例来逐步了解Model。

先定义一个页面结构，实践时须在注释的地方填上各小节的代码

.. code:: html
    
    <!DOCTYPE html>
    <html>
    <head>
    <title>the5fire-backbone-model</title>
    </head>
    <body>
    </body>
    <script src="http://the5fireblog.b0.upaiyun.com/staticfile/jquery-1.10.2.js"></script>
    <script src="http://the5fireblog.b0.upaiyun.com/staticfile/underscore.js"></script>
    <script src="http://the5fireblog.b0.upaiyun.com/staticfile/backbone.js"></script>
    <script>
    (function ($) {
        /**
        *此处填充代码下面练习代码
        **/
    })(jQuery);
    </script>
    </html> 

2.1 最简单的对象
--------------------------

.. code:: javascript

    var Man = Backbone.Model.extend({
        initialize: function(){
            alert('Hey, you create me!');
        }
    });
    var man = new Man;

这个确实很简单了，只是定义了一个最基础的Model，只是实现了initialize这个初始化方法，也称构造函数。这个函数会在Model被实例化时调用。

2.2 对象属性赋值的两种方法
------------------------------------
第一种，直接定义，设置默认值。

.. code:: javascript

    var Man = Backbone.Model.extend({
        initialize: function(){
            alert('Hey, you create me!');
        },
        defaults: {
            name:'张三',
            age: '38'
        }
    });
    
    var man = new Man;
    alert(man.get('name'));

第二种，赋值时定义

.. code:: javascript

    var Man = Backbone.Model.extend({
        initialize: function(){
            alert('Hey, you create me!');
        }
    });
    var man = new Man;
    man.set({name:'the5fire',age:'10'});
    alert(man.get('name'));

从这个对象的取值方式可以知道，属性在一个Model是以字典（或者类似字典）的方式存在的，第一种设定默认值的方式，只不过是实现了Backbone的defaults这个方法，或者是给defaults进行了赋值。


2.3 对象中的方法
-----------------------------

.. code:: javascript

    var Man = Backbone.Model.extend({
        initialize: function(){
            alert('Hey, you create me!');
        },
        defaults: {
            name:'张三',
            age: '38'
        },
        aboutMe: function(){
            return '我叫' + this.get('name') + ',今年' + this.get('age') + '岁';
        }
    });
    var man = new Man;
    alert(man.aboutMe());

也是比较简单，只是增加了一个新的属性，值是一个function。说到这，不知道你是否发现，在所有的定义或者赋值操作中，都是通过字典的方式来完成的，比如extend Backbone的Model，以及定义方法，定义默认值。方法的调用和其他的语言一样，直接 ``.`` 即可，参数的定义和传递也一样。


2.4 监听对象中属性的变化
--------------------------------

假设你有在对象的某个属性发生变化时去处理一些业务的话，下面的示例会有帮助。依然是定义那个类，不同的是我们在构造函数中绑定了name属性的change事件。这样当name发生变化是，就会触发这个function。

.. code:: javascript

    var Man = Backbone.Model.extend({
        initialize: function(){
            alert('Hey, you create me!');
            //初始化时绑定监听
            this.bind("change:name",function(){
                var name = this.get("name");
                alert("你改变了name属性为：" + name);
            });
        },
        defaults: {
            name:'张三',
            age: '38'
        },
        aboutMe: function(){
            return '我叫' + this.get('name') + ',今年' + this.get('age') + '岁';
        }
    });
    var man = new Man;
    man.set({name:'the5fire'})  //触发绑定的change事件，alert。
    man.set({name:'the5fire.com'})  //触发绑定的change事件，alert。


2.5 为对象添加验证规则，以及错误提示
----------------------------------------------

.. code:: javascript

    var Man = Backbone.Model.extend({
        initialize: function(){
            alert('Hey, you create me!');
            //初始化时绑定监听, change事件会先于validate发生
            this.bind("change:name",function(){
                var name = this.get("name");
                alert("你改变了name属性为：" + name);
            });
            this.bind("invalid",function(model,error){
                alert(error);
            });
        },
        defaults: {
            name:'张三',
            age: '38'
        },
        validate:function(attributes){
            if(attributes.name == '') {
                return "name不能为空！";
            }
        },
        aboutMe: function(){
            return '我叫' + this.get('name') + ',今年' + this.get('age') + '岁';
        }
    });
    var man = new Man;
    // 这种方式添加错误处理也行
    // man.on('invalid', function(model, error){
    //         alert(error);
    // });

    man.set({name:''}); //默认set时不进行验证
    //man.set({name:''}, {'validate':true});  //手动触发验证, set时会触发
    man.save(); //save时触发验证。根据验证规则，弹出错误提示。

2.6 和服务器进行交互，对象的保存和获取
---------------------------------------------------
首先需要声明的是，这个例子需要后端配合，可以在 `code <../code>`_  目录中找到对应的py文件，需要webpy和mako这两个库。
这里需要为对象定义一个url属性，调用save方法时会post对象的所有属性到server端，调用fetch方法是又会发送get请求到server端。接受数据和发送数据均为json格式:

.. code:: javascript

    var Man = Backbone.Model.extend({
        url:'/man/',
        initialize: function(){
            alert('Hey, you create me!');
            //初始化时绑定监听
            this.bind("change:name",function(){
                var name = this.get("name");
                alert("你改变了name属性为：" + name);
            });
            this.bind("error",function(model,error){
                alert(error);
            });
        },
        defaults: {
            name:'张三',
            age: '38'
        },
        validate:function(attributes){
            if(attributes.name == '') {
                return "name不能为空！";
            }
        },
        aboutMe: function(){
            return '我叫' + this.get('name') + ',今年' + this.get('age') + '岁';
        }
    });
    var man = new Man;;
    man.set({name:'the5fire'});
    man.save();  //会发送POST到模型对应的url，数据格式为json{"name":"the5fire","age":38}
    //然后接着就是从服务器端获取数据使用方法fetch([options])
    var man1 = new Man;
    //第一种情况，如果直接使用fetch方法，那么他会发送get请求到你model的url中，
        //你在服务器端可以通过判断是get还是post来进行对应的操作。
    man1.fetch();
    //第二种情况，在fetch中加入参数，如下：
    man1.fetch({url:'/man/'});
    //这样，就会发送get请求到/getmans/这个url中，
    //服务器返回的结果样式应该是对应的json格式数据，同save时POST过去的格式。

    //不过接受服务器端返回的数据方法是这样的：
    man1.fetch({url:'/man/',
        success:function(model,response){
            alert('success');
            //model为获取到的数据
            alert(model.get('name'));
        },error:function(){
            //当返回格式不正确或者是非json数据时，会执行此方法
            alert('error');
        }
    });

还有一点值得一提的是关于url和urlRoot的事情了，如果你设置了url，那么你的CRUD都会发送对应请求到这个url上，但是这样有一个问题，就是delete请求，发送了请求，但是却没有发送任何数据，那么你在服务器端就不知道应该删除哪个对象（记录），所以这里又一个urlRoot的概念，你设置了urlRoot之后，你发送PUT和DELETE请求的时候，其请求的url地址就是：/baseurl/[model.id]，这样你就可以在服务器端通过对url后面值的提取更新或者删除对应的对象（记录）

补充一点，就是关于服务器的异步操作都是通过Backbone.sync这个方法来完成的，调用这个方法的时候会自动的传递一个参数过去，根据参数向服务器端发送对应的请求。比如你save，backbone会判断你的这个对象是不是新的，如果是新创建的则参数为create，如果是已存在的对象只是进行了改变，那么参数就为update，如果你调用fetch方法，那参数就是read，如果是destory，那么参数就是delete。也就是所谓的CRUD ("create", "read", "update", or "delete")，而这四种参数对应的请求类型为POST，GET，PUT，DELETE。你可以在服务器根据这个request类型，来做出相应的CRUD操作。

关于Backbone.sync在后面会有如何自定义这一部分的章节。

上面服务器端的代码在 ``code`` 下可以找到，基于webpy和mako的。


**导航**

* 上一章 01  `Hello Backbonejs <01-hello-backbonejs.rst>`_
* 下一章 03  `Backbonejs中的Collections实践 <03-backbonejs-collection.rst>`_
