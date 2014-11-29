'use strict';

angular.module('radsquaredApp')
  .factory('Session', function ($resource) {
    return $resource('/api/session/');
  });
