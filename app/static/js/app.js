/** Main AngularJS app config file **/
'use strict';

var app = angular.module('testApp', ['ngRoute', 'ngResource']);

app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/songs', {
                templateUrl: 'static/html/song/song.html',
                controller: 'songController',
                controllerAs: 'songCon'
            }).
            otherwise({
                redirectTo: '/songs'
            });

    }]);


app.controller("testController", function() {
    var self = this;

    self.message = "Wechanged soemthtingnggn";
});