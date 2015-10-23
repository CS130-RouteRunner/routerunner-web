/** Main AngularJS app config file **/
'use strict';

var app = angular.module('testApp', ['ngRoute', 'ngResource']);

app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/songs', {
                templateUrl: 'static/html/map/map.html',
                controller: 'mapController',
                controllerAs: 'mapCon'
            }).
            otherwise({
                redirectTo: '/songs'
            });

    }]);


app.controller("testController", function() {
    var self = this;

    self.message = "Wechanged soemthtingnggn";
});