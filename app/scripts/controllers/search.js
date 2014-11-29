'use strict';

var myApp = angular.module('radsquaredApp');

myApp.controller('SearchCtrl', function ($rootScope, $scope, $http, $document, $cookieStore) {

  var easeInOutQuad = function (t) { return t<0.5 ? 2*t*t : -1+(4-2*t)*t; };

  $scope.idArray = [];
  $scope.numResults = 0;
  $scope.numPerPage = 5;
  $scope.maxNumSnippets = $cookieStore.get('maxNumSnippets') || 20;
  $scope.nightMode = $cookieStore.get('nightMode') || false;
  $scope.textSizePercent = $cookieStore.get('textSizePercent') || 100;
  $scope.page = 1;
  $scope.items = []; // array of returned snippet items (json objects)
  $scope.upvotingUserByItem = []; // array corresponding to items indicating if user upvoted
  $scope.downvotingUserByItem = []; // array corresponding to items indicating if user downvoted
  $scope.started = false;
  $scope.ended = false;
  $scope.busy = false;
  $scope.settingsShow = false;

  $scope.fetchAllIds = function() {
    if ($scope.busy) {
      return;
    }

    if ($scope.inputText) {

      $scope.page = 1;
      $scope.items = [];
      $scope.upvotingUserByItem = [];
      $scope.downvotingUserByItem = [];
      $scope.busy = true;

      var input = {
        'inputText': $scope.inputText,
        'limit': $scope.maxNumSnippets
      };
      $http.post('/api/fetchRelevant', input).
        success(function(idArray) {
          $scope.idArray = idArray;
          $scope.numResults = idArray.length;
          $scope.started = true;
          $scope.ended = false;
          $scope.busy = false;
          $scope.nextPage();
          $document.scrollToElement(angular.element(document.getElementById('snippetRoll')), 70, 800, easeInOutQuad);
        }).
        error(function(err) {
          console.log(err);
          $scope.started = false;
          $scope.ended = true;
          $scope.busy = false;
        });

    }
  };

  $scope.nextPage = function () {
    if ($scope.busy || $scope.ended) {
      return;
    }
    $scope.busy = true;
    
    var idArraySlice = $scope.idArray.slice(($scope.page - 1) * $scope.numPerPage, $scope.page * $scope.numPerPage);
    if ($rootScope.currentUser) {
      var userId = $rootScope.currentUser._id;
    }

    $http.post('/api/getSnippetByIds', {'idArray': idArraySlice}).success(function(results) {

      if ($rootScope.currentUser) {

        $http.post('/api/getUpvotedIds', {'idArray': idArraySlice, 'userId': userId})
          .success(function (upvotedIds) {
            var ids = [];
            upvotedIds.forEach(function (objId) {
              ids.push(objId._id);
            });
            for (var i = 0; i < results.length; i++) {
              $scope.upvotingUserByItem.push(ids.indexOf(results[i]._id) !== -1);
            }
          });

        $http.post('/api/getDownvotedIds', {'idArray': idArraySlice, 'userId': userId})
          .success(function (downvotedIds) {
            var ids = [];
            downvotedIds.forEach(function (objId) {
              ids.push(objId._id);
            });
            for (var i = 0; i < results.length; i++) {
              $scope.downvotingUserByItem.push(ids.indexOf(results[i]._id) !== -1);
            }
          });
        
      }

      for (var i = 0; i < results.length; i++) {
        $scope.items.push(results[i]);
      }
      angular.forEach($scope.items, function(item, index){
        item.index = index;
      });

      if ($scope.page * $scope.numPerPage >= $scope.numResults) {
        $scope.ended = true;
      } else {
        $scope.page += 1;
      }

      $scope.busy = false;
    });

  };

  $scope.returnToTop = function () {
    $document.scrollToElement(angular.element(document.getElementById('inputTextDiv')), 70, 400, easeInOutQuad);
  };

  $scope.upvoteSnippet = function (index) {
    var userId = $rootScope.currentUser._id;
    var docId = $scope.items[index]._id;
    $http.post('/api/upvoteSnippet', {'docId': docId, 'userId': userId}).success(function () {
      $scope.upvotingUserByItem[index] = true;
      $scope.items[index].upvotes += 1;
    });
  };

  $scope.downvoteSnippet = function (index) {
    var userId = $rootScope.currentUser._id;
    var docId = $scope.items[index]._id;
    $http.post('/api/downvoteSnippet', {'docId': docId, 'userId': userId}).success(function () {
      $scope.downvotingUserByItem[index] = true;
      $scope.items[index].downvotes += 1;
    });
  };

  $scope.saveSettings = function() {
    $scope.settingsShow = false;
    $cookieStore.put('maxNumSnippets', $scope.maxNumSnippets);
    $cookieStore.put('textSizePercent', $scope.textSizePercent);
    $cookieStore.put('nightMode', $scope.nightMode);
  };

  $scope.customFilter = function(item) {
    var isItemDisplayed = true;
    if ($scope.filterSnippetsUpvoted) {
      isItemDisplayed = isItemDisplayed && (item.upvotes > 0);
    }
    if ($scope.filterSnippetsWithFigs) {
      isItemDisplayed = isItemDisplayed && (item.docSubtype === 'figure');
    }
    return isItemDisplayed;
  };

  $scope.saveQuery = function() {
    var userId;
    if ($rootScope.currentUser) {
      userId = $rootScope.currentUser._id;
    }
    var queryData = {'query': $scope.inputText, 'userId': userId, 'dateSubmitted': Date.now()};
    $http.post('/api/saveQuery', queryData).success(function (data) {
      $scope.saveQueryMsg = 'Query successfully saved.';
    }).error(function (err) {
      $scope.saveQueryMsg = err;
    });
  };


  /*
   * fetches the selected query from rootScope (i.e., from a user's saved queries list)
   */
  if ($rootScope.selectedQuery) {
    $scope.inputText = $rootScope.selectedQuery;
    $scope.fetchAllIds();
  }

});