'use strict';

app.controller("matchmakingController", function(newLobbyResource, joinLobbyResource, startGameResource){
    var self = this;
    self.message = "Matchmaking Controller";
    self.showLobby = false;
    self.messages = [];
    self.lobbies = joinLobbyResource.get(function(resp) {
        self.lobbies = resp.lobbies;
    });

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
        var request = {uid: user};

        newLobbyResource.save(angular.toJson(request), function(success) {
            self.success = success.data;
            self.lobbyId = success.lid;
            self.lobbies.push(self.lobbyId);
        }, function(failure) {
            self.error = failure.data;
        });
    };

    self.joinLobby = function(lobby_id) {
        var user = randomString();
        var request = {lid: lobby_id, uid: user};
        joinLobbyResource.save(angular.toJson(request), function(success) {
            self.success = success.data;
        }, function(failure) {
            self.error = failure.data;
        });
    };
});
