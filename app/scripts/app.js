'use strict';

angular.module('radsquaredApp', [
  'ngCookies',
  'ngResource',
  'ngSanitize',
  'ngRoute',
  'infinite-scroll',
  'angular-inview',
  'duScroll',
  'ui.bootstrap',
  'ngTable'
])
  .config(function ($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'partials/search',
        controller: 'SearchCtrl'
      })
      .when('/search', {
        templateUrl: 'partials/search',
        controller: 'SearchCtrl'
      })
      .when('/contribute', {
        templateUrl: 'partials/contribute',
        controller: 'ContributeCtrl'
      })
      .when('/mylibrary', {
        templateUrl: 'partials/mylibrary',
        controller: 'MyLibraryCtrl'
      })
      .when('/about', {
        templateUrl: 'partials/about',
        controller: 'AboutCtrl'
      })
      .when('/privacy', {
        templateUrl: 'partials/privacy',
        controller: 'AboutCtrl'
      })
      .when('/tos', {
        templateUrl: 'partials/tos',
        controller: 'AboutCtrl'
      })
      .when('/login', {
        templateUrl: 'partials/login',
        controller: 'LoginCtrl'
      })
      .when('/signup', {
        templateUrl: 'partials/signup',
        controller: 'SignupCtrl'
      })
      .when('/account', {
        templateUrl: 'partials/account',
        controller: 'AccountCtrl',
        authenticate: true
      })
      .otherwise({
        redirectTo: '/'
      });
      
    $locationProvider.html5Mode(true);
      
    // Intercept 401s and redirect you to login
    $httpProvider.interceptors.push(['$q', '$location', function($q, $location) {
      return {
        'responseError': function(response) {
          if(response.status === 401) {
            $location.path('/login');
            return $q.reject(response);
          }
          else {
            return $q.reject(response);
          }
        }
      };
    }]);
  })
  .run(function ($rootScope, $location, Auth) {

    // Redirect to login if route requires auth and you're not logged in
    $rootScope.$on('$routeChangeStart', function (event, next) {
      
      if (next.authenticate && !Auth.isLoggedIn()) {
        $location.path('/login');
      }
    });
  });