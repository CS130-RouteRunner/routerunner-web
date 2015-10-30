'use strict';

app.controller("matchmakingController", function(newLobbyResource, joinLobbyResource, startGameResource, initGameResource){
    var self = this;
    self.message = "Matchmaking Controller";
    self.showLobby = false;
    self.messages = [];
    self.lobbies = joinLobbyResource.get(function(resp) {
        self.lobbies = resp.lobbies;
    });
    self.user = "";

    function randomString() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for( var i = 0; i < 5; i++) {
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        }
        return text;
    }

    self.createLobby = function() {
        var user = randomString();
        var request = {uid: user, lid: "routerunner-" + user};

        newLobbyResource.save(angular.toJson(request), function(success) {
            self.success = success;
        }, function(failure) {
            self.error = failure;
        });
    };

    self.joinLobby = function(lobby_id) {
        var user = randomString();
        var request = {lid: lobby_id, uid: user};
        joinLobbyResource.save(angular.toJson(request), function(success) {
            self.success = success;
        }, function(failure) {
            self.error = failure;
        });
    };

    self.startGame = function(lobby_id) {
        var request = {lid: lobby_id, uid: self.user};
        startGameResource.save(angular.toJson(request), function(success) {
            self.success = success;
            self.ready = self.success.ready;
            alert(self.ready);
        }, function(failure) {
            self.error = failure;
        });
    };
    self.initGame = function(lobby_id, route_data)
        var request = {uid: self.user cid: lobby_id, current_gold: '100', route: route_data.info}
        initGameResource.save(angular.toJson(request), function(success) {
            self.success = success.data;
            route = route_data.info;
            self.route = success[route];
            self.messages.push("Your route is " + self.route);
        }, function(failure) {
            self.error = failure.data;
        });
});
