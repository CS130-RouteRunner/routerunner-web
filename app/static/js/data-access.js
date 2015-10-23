/** Resources to hit API endpoints **/
'use strict';

app.factory('mapResource', function($resource){
   return $resource('/api/map');
});
