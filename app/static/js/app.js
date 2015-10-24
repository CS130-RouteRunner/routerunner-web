/** Main AngularJS app config file **/
'use strict';

var app = angular.module('routeRunner', ['ngRoute', 'ngResource']);

app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/maps', {
                templateUrl: 'static/html/map/map.html',
                controller: 'mapController',
                controllerAs: 'mapCon'
            }).
            when('/matchmaking', {
                templateUrl: 'static/html/matchmaking/lobby.html',
                controller: 'matchmakingController',
                controllerAs: 'matchmakingCon'
            }).
            when('/', {
                templateUrl: 'static/html/index.html'
            }).
            otherwise({
                redirectTo: '/maps'
            });

    }]);


app.controller("mainController", function($http) {
    var self = this;

    self.message = "Wechanged soemthtingnggn";

});
