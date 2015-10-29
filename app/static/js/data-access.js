/** Resources to hit API endpoints **/
'use strict';

var MATCHMAKING_BASE_URL = '/api/matchmaking/';

app.factory('mapResource', function($resource){
   return $resource('/api/map');
}).factory('newLobbyResource', function($resource){
   return $resource(MATCHMAKING_BASE_URL + 'new');
}).factory('joinLobbyResource', function($resource){
    return $resource(MATCHMAKING_BASE_URL + 'join');
}).factory('startGameResource', function($resource){
    return $resource(MATCHMAKING_BASE_URL + 'start');
}).factory('endGameResource', function($resource){
    return $resource(MATCHMAKING_BASE_URL + 'end');
});
