'use strict';

app.controller("matchmakingController", function(newLobbyResource, joinLobbyResource, startGameResource){
    var self = this;
    self.message = "Matchmaking Controller";
    self.showLobby = false;
    self.messages = [];
    self.lobbies = joinLobbyResource.query(function() {});

    self.createLobby = function() {
        var user_id = {uid: '12345'};
        newLobbyResource.save(angular.toJson(user_id), function(success) {
            self.success = success.data;
            self.lobbyId = success['lobby-id'];
            self.messages.push("Welcome to routerunner-" + self.lobbyId);
            self.lobbies.push(self.lobbyId);
            self.showLobby = true;

        }, function(failure) {
            self.error = failure.data;
        });
    };

    self.joinLobby = function(lobby_id) {
        joinLobbyResource.save(angular.toJson({cid: lobby_id}), function(success) {
            self.success = success.data;
            self.messages.push("Someone has joined the lobby");
            self.showLobby = true;
        }, function(failure) {
            self.error = failure.data;
        });

        //var channel_id = {cid: 'routerunner-12345'};
        //newLobbyResource.save(angular.toJson(channel_id), function(success) {
        //    self.success = success.data;
        //    self.messages.push("Someone has joined the lobby");
        //    self.showLobby = true;
        //}, function(failure) {
        //    self.error = failure.data;
        //});
    };
});
