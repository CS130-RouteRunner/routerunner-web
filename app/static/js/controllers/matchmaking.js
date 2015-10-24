'use strict';

app.controller("matchmakingController", function($http){
    var self = this;
    self.message = "Matchmaking Controller";

    $http.get('/api/matchmaking');

});
