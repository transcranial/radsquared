'use strict';

var myApp = angular.module('radsquaredApp');

myApp.controller('NavbarCtrl', function ($scope, $location, Auth) {
  $scope.menu = [{
    'title': 'About',
    'link': '/about'
  }];
  
  $scope.logout = function() {
    Auth.logout()
    .then(function() {
      $location.path('/login');
    });
  };
  
  $scope.isActive = function(route) {
    return route === $location.path();
  };
});
