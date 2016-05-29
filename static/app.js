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
  $scope.ruler = 0;
  $scope.seismic = [];
  $scope.usermodel = [];
  $scope.userseismic = [];
  $scope.realmodel = [];
  $scope.showRealModel = false;
  $scope.dataRange = [-0.6,0.6];
  
  $scope.doTry = function() {
      $scope.tries -= 1;
      
      var data = {usermodel: $scope.usermodel};
      $http.post('/api/forward', data, {headers: {'Content-Type': 'application/json'}})
        .then(function(resp) {
          $scope.userseismic = resp.data.seismic;
          $('#userseismic svg').remove();
          plotWiggles('#userseismic', $scope.userseismic, $scope.dataRange); 
        })
  }
  
  $scope.doReveal = function() {
    $scope.showRealModel = true;
  }
  
  $http({method: 'GET', url: '/api/model/' + $stateParams.level})
    .then(function(response) {
      $scope.seismic = response.data.seismic;
      $scope.realmodel = response.data.reflectivity;
      if (response.data.min)
        $scope.dataRange = [response.data.min, response.data.max];
      
      plotWiggles('#seismic', $scope.seismic, $scope.dataRange);
      $scope.realModelChart = createBarPlot($scope, '#realmodelchart', $scope.realmodel);

    }, function(response) {
      alert(response.error)
    });
  
  for (var i = 0; i < 300; i++)
    $scope.usermodel.push(0)
 
  $scope.userModelChart = createBarPlot($scope, '#usermodelchart', $scope.usermodel);
  
})

function createBarPlot($scope, selector, dataset) {
   var margin = {top: 30, right: 30, bottom: 20, left: 30}; 
  var width = 270 - margin.left - margin.right,
    height = 630 - margin.top - margin.bottom;
  
    var svg = d3.select(selector)
    .append('svg')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);
    
    svg = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    render($scope, svg, dataset, width, height);
    
    return svg;
}


function render($scope, svg, dataset, width, height) {
  var numSamples = dataset.length;
  var barHeight = height/numSamples;
  
  var extent = d3.max([Math.abs($scope.dataRange[0]), $scope.dataRange[1]]);
  var xScale = d3.scale.linear()
    .domain([0, extent])
    .range([0, width/2])
  var yAxisScale = d3.scale.linear()
    .domain([0, numSamples])
    .range([0, height]);

  svg.append("rect")
        .attr({"class": "overlay"})
        .attr("width", width)
        .attr("height", height)
        .on({
          "mousemove":  function() {
            var coords = d3.mouse(this);
            $scope.ruler = Math.round(yAxisScale.invert(coords[1]));
            $scope.$apply();
          }, 
          "click":  function() {
            var coords = d3.mouse(this);
            var p = {
              x: xScale.invert(coords[0]) - extent,
              y: Math.round( yAxisScale.invert(coords[1]) )
            };
            dataset[p.y] = p.x;
            $('#usermodelchart svg').remove();
            createBarPlot($scope, '#usermodelchart', dataset);
          }, 
        });
    
  svg.selectAll("rect")
    .data(dataset)
    .enter().append("rect")
    .attr("x", function(d) {
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

  var xAxisScale = d3.scale.linear()
    .domain([-extent, extent])
    .range([0, width])
  var xAxis = d3.svg.axis();
  xAxis.scale(xAxisScale).orient("top");
  svg.append("g")
    .attr("class", "axis")
    .call(xAxis);
  
  var yAxis = d3.svg.axis();
    yAxis.scale(yAxisScale).orient("left");
    svg.append("g")
      .attr("class","axis")
      .call(yAxis);
 
}