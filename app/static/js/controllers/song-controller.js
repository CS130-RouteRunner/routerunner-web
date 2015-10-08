'use strict';

app.controller("songController", function($http, songResource) {
    var self = this;

    self.getSong = function(id) {
        self.song = songResource.get({'id': id});
    };

    self.addSong = function(song) {
        song = {title: 'Roger', artist: 'Roger', duration: '60', genre: 'rap'};
        songResource.save(angular.toJson(song), function(success) {
            self.success = success.data;
        }, function(failure) {
            self.error = failure.data;
        });
    };
});
