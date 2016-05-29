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
 
 
function plotWiggles(selector, data, range) {
   var wigglePlot = g3.plot(selector)
    .height(580)
    .xTicks(7)
    .xDomain(range)
    .yDomain([0, data.length])
    .draw();
  
  var wig = g3.wiggle(wigglePlot, [data])
    .xTrans(0)
    .draw();
} 
 
myApp.controller('GameController',function($scope, $stateParams, $http) {
  $scope.tries = 5;
    
  $scope.seismic = [];
  $scope.model = [];
  
  $http({method: 'GET', url: '/api/model/1'})
    .then(function(response) {
      $scope.seismic = response.data.seismic;
      $scope.model = response.data.model;
      
      plotWiggles('#seismic', $scope.seismic, [-0.6, 0.6]);
      plotWiggles('#userseismic', $scope.seismic, [-0.6, 0.6]);

    }, function(response) {
      alert(response.error)
    });
  
 var margin = {top: 30, right: 10, bottom: 20, left: 15}; 
  var width = 270 - margin.left - margin.right,
    height = 580 - margin.top - margin.bottom;
  
  var numSamples = 100
  var barHeight = height/numSamples;
  var dataset = []
  for (var i = 0; i < numSamples; i++)
    dataset.push(0)  
  
  dataset[0] = 0.1;
  dataset[1] = -0.2;
  dataset[2] = 0.3;
  dataset[3] = -0.4;
  dataset[4] = 0.5;
  dataset[5] = -0.6;
  dataset[6] = 0.7;
  dataset[7] = -0.8;
  dataset[8] = 0.9;
  dataset[9] = -1.0;
  // dataset[2] = -0.1;
  // dataset[3] = -1;

 

  var svg = d3.select('#usermodelchart')
    .append('svg')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  console.log(d3.min(dataset))
  var extent = d3.max([Math.abs(d3.min(dataset)), d3.max(dataset)]);
  var xScale = d3.scale.linear()
    .domain([0, extent])
    .range([0, width/2])
    
  svg.selectAll("rect")
    .data(dataset)
    .enter().append("rect")
    .attr("x", function(d) {
      console.log(d) 
      if (d >= 0)
        return (width/2);
      else
        return (width/2) + xScale(d);
     })
    .attr("y", function(d, i) {
      return i * barHeight;
    })
    .attr("width", function(d) { 
      if (d < 0) d *= -1;
      return xScale(d);
    })
    .attr('height', barHeight - 1);
      
  svg.on("click", function() {
    var coords = d3.mouse(this);
    
  })

  var xAxisScale = d3.scale.linear()
    .domain([-extent, extent])
    .range([0, width])
  var xAxis = d3.svg.axis();
  xAxis.scale(xAxisScale).orient("top");
  svg.append("g")
    .attr("class", "axis")
    .call(xAxis);
  


})