var myApp = angular.module('hinv', ['ui.router']);

myApp.config(function($stateProvider, $urlRouterProvider) {
  //
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/");
  //
  // Now set up the states
  $stateProvider
    .state('home', {
      url: "/",
      templateUrl: "partials/start.html"
    })
    .state('game', {
      url: "/game/:level",
      templateUrl: "partials/game.html",
      controller: function($scope, $stateParams) {
        console.log("level", $stateParams.level)
      }
    })
    .state('test', {
      url: "/test",
      templateUrl: "partials/test.html"
    })
    .state('state2.list', {
      url: "/list",
      templateUrl: "partials/state2.list.html",
      controller: function($scope) {
        $scope.things = ["A", "Set", "Of", "Things"];
      }
    });
});