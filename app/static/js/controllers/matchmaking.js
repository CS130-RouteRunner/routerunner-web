'use strict';

app.controller("matchmakingController", function(newLobbyResource, joinLobbyResource, startGameResource){
    var self = this;
    self.message = "Matchmaking Controller";
    self.showLobby = false;
    self.messages = [];
    self.lobbies = joinLobbyResource.query(function() {});
    console.log(self.lobbies);

    self.createLobby = function() {
        var user_id = {uid: '72cf413c-324e-4ec2-b04b-6e6eee969a08'};
        newLobbyResource.save(angular.toJson(user_id), function(success) {
            self.success = success.data;
            self.lobbyId = success['lobby-id'];
            self.messages.push("Welcome to routerunner-" + self.lobbyId);
            //self.lobbies.push(self.lobbyId);
            self.showLobby = true;
        }, function(failure) {
            self.error = failure.data;
        });
    };

    self.joinLobby = function(lobby_id) {
        var request = {cid: lobby_id, uid: "cff9ea12-2fe4-40fc-b237-96e42bced00e"};
        joinLobbyResource.save(angular.toJson(request), function(success) {
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
