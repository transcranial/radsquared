'use strict';

var myApp = angular.module('radsquaredApp');

myApp.directive('collapseOnScroll', function ($window) {
  return function(scope, element, attrs) {
    var $page = angular.element($window);
    var $el = element[0];
    var elTop = $el.getBoundingClientRect().top - 30;
    var elHeight = $el.clientHeight;

    $page.bind('scroll', function () {
      var windowScrollTop = this.pageYOffset;

      if (windowScrollTop > elTop) {
        element.css('position', 'fixed').css('height', attrs.collapseOnScroll + 'px');
      } else {
        element.css('position', 'relative').css('height', elHeight + 'px');
      }
    });
  };
});