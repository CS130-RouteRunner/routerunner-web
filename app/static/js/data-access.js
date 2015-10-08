/** Resources to hit API endpoints **/
'use strict';

app.factory('songResource', function($resource){
   return $resource('/api/song');
});