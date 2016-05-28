var myApp = angular.module('hinv', ['ui.router','n3-line-chart']);

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
      controller: 'GameController'
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
 
myApp.controller('GameController',function($scope, $stateParams, $http) {
  
  $scope.seismic = [];
  $scope.model = [];
  // for (var i = 0; i < 256; i++) {
  //   $scope.seismic.push(Math.sin(2*Math.PI*i/64))
  // }
  
  $http({method: 'GET', url: '/api/model/1'})
    .then(function(response) {
      $scope.seismic = response.data.seismic;
      $scope.model = response.data.model;
      
    var wigglePlot = g3.plot('#realseismic')
      .height(400)
      .xDomain([-1, 1])
      .yDomain([0, $scope.seismic.length])
      .draw();
    
    var wig = g3.wiggle(wigglePlot, [$scope.seismic])
      .xTrans(0)
      .draw();
  
    var wigglePlot = g3.plot('#userseismic')
      .height(400)
      .xDomain([-1, 1])
      .yDomain([0, $scope.seismic.length])
      .draw();
    
    var wig = g3.wiggle(wigglePlot, [$scope.seismic])
      .xTrans(0)
      .draw();
      
      
      
    }, function(response) {
      alert(response.error)
    })
  
  


  
  $scope.tries = 5;
  
  $scope.data = {
    seismic: [
      {x:0, val_0: 10},
      {x:1, val_0: 15},
      {x:2, val_0: 18}
    ]
  };
  
  $scope.seismicOptions = {
      series: [
        {
          axis: "x",
          dataset: "seismic",
          key: "val_0",
          label: "Seismic Series",
          color: "#ff0000",
          type: ['column'],
          id: "seismic",
          visible:true
        }
      ],
      axes: { y: { key: "x"} }
  };

})