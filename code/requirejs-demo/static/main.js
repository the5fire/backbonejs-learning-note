require.config({
    baseUrl: 'static/',
    // ref: http://www.ruanyifeng.com/blog/2012/11/require_js.html
    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        backboneLocalstorage: {
            deps: ['backbone'],
            exports: 'Store'
        }
    },
    paths: {
        jquery: 'lib/jquery',
        underscore: 'lib/underscore',
        backbone: 'lib/backbone'
    }
});

require(['jquery', 'backbone', 'js/app'], function($, Backbone, AppView) {
    var appView = new AppView();
});
