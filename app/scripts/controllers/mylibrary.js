'use strict';

var myApp = angular.module('radsquaredApp');

myApp.controller('MyLibraryCtrl', function ($rootScope, $scope, $location, $http, $filter, ngTableParams) {

  if ($rootScope.currentUser) {

    $scope.userId = $rootScope.currentUser._id;
    
    $http.get('/api/getUserQueries/' + $scope.userId).success(function (data) {
      $scope.userQueries = data;

      $scope.tableParams = new ngTableParams({
            page: 1,            // show first page
            count: 10,          // count per page
            sorting: {
                date: 'asc'     // initial sorting
            }
          }, {
            total: $scope.userQueries.length, // length of data
            getData: function($defer, params) {
              // use build-in angular filter
              var orderedData = params.sorting() ? $filter('orderBy')($scope.userQueries, params.orderBy()) : $scope.userQueries;

              $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
          }
        });
    }).error(function (err) {
      $scope.userQueries = err;
    });

    $rootScope.selectedQuery = '';
    $scope.fetchQuery = function (index) {
      $rootScope.selectedQuery = $scope.userQueries[index].query;
      $location.path('/');
    };

  }

});