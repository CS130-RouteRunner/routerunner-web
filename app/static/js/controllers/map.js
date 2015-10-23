'use strict';

app.controller("mapController", function($http, mapResource) {
    var self = this;
    self.accessToken = 'pk.eyJ1IjoicmNoZW45MyIsImEiOiJjaWcyeDZ1NzExZ3FidGxreHpiNG5neTV5In0.0ZjmL0S4tNln-Op6vQzuRQ';
    self.mapCenter = [34.068921, -118.4473698,17];
    self.defaultZoomLevel = 15;
    self.decimalPrecision = 5;  // 4 decimal points

    // Provide your access token
    L.mapbox.accessToken = self.accessToken;
    // Create a map in the div #map
    self.map = L.mapbox.map('map', 'mapbox.streets').setView(self.mapCenter, self.defaultZoomLevel);

    // Features we can add to map
    var featureGroup = L.featureGroup().addTo(self.map);
    var markers = [];

    // Draw the feature
    var drawControl = new L.Control.Draw({
        edit: {
                featureGroup: featureGroup
            }
    }).addTo(self.map);

    // Add feature as a layer
    self.map.on('draw:created', function(e) {
        featureGroup.addLayer(e.layer);
        var lat = e.layer._latlng.lat.toString();
        var lng = e.layer._latlng.lng.toString();
        lat = lat.slice(0, lat.indexOf(".") + self.decimalPrecision);
        lng = lng.slice(0, lng.indexOf(".") + self.decimalPrecision);
        markers.push(lng + "," + lat);

        if (markers.length === 2) {
            var waypoints = {'lng': markers[0], 'lat': markers[1]};
            mapResource.get({'waypoints': angular.toJson(waypoints)}, function(resp) {
                self.route = resp;
                L.geoJson(self.route, {style: L.mapbox.simplestyle.style}).addTo(self.map);
                var start = [10, 20];
                var momentum = [3, 3];

                for (var i = 0; i < 300; i++) {
                    start[0] += momentum[0];
                    start[1] += momentum[1];
                    if (start[1] > 60 || start[1] < -60) {
                        momentum[1] *= -1;
                    }
                    if (start[0] > 170 || start[0] < -170) {
                        momentum[0] *= -1;
                    }
                    self.route.coordinates.push(start.slice());
                }

                // Create a counter with a value of 0.
                var j = 0;

                // Create a marker and add it to the map.
                var marker = L.marker([0, 0], {
                    icon: L.mapbox.marker.icon({
                        'marker-color': '#f86767'
                    })
                }).addTo(self.map);

                tick();
                function tick() {
                    // Set the marker to be at the same point as one
                    // of the segments or the line.
                    marker.setLatLng(L.latLng(
                        self.route.coordinates[j][1],
                        self.route.coordinates[j][0]));

                    // Move to the next point of the line
                    // until `j` reaches the length of the array.
                    if (++j < self.route.coordinates.length) {
                        setTimeout(tick, 100);
                    }
                }
            });
        }

    });


    //self.getSong = function(id) {
    //    self.song = mapResource.get({'id': id});
    //};
    //
    //self.addSong = function(song) {
    //    song = {title: 'Roger', artist: 'Roger', duration: '60', genre: 'rap'};
    //    mapResource.save(angular.toJson(song), function(success) {
    //        self.success = success.data;
    //    }, function(failure) {
    //        self.error = failure.data;
    //    });
    //};


});
