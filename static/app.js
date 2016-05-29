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
  
  $scope.doTry = function() {
      $scope.tries -= 1;
      
      var data = {usermodel: $scope.usermodel};
      console.log(data)
      $http.post('/api/forward', data, {headers: {'Content-Type': 'application/json'}})
        .then(function(resp) {
          console.log(resp)
          $scope.userseismic = resp.data.seismic;
          $('#userseismic svg').remove();
          plotWiggles('#userseismic', $scope.userseismic, [-0.6, 0.6]); 
        }, function(err) {
          alert('Bang!')
        })
  }
  
  $scope.doReveal = function() {
    $scope.showRealModel = true;
  }
  
  $http({method: 'GET', url: '/api/model/' + $stateParams.level})
    .then(function(response) {
      $scope.seismic = response.data.seismic;
      $scope.realmodel = response.data.reflectivity;
      
      plotWiggles('#seismic', $scope.seismic, [-0.6, 0.6]);
      $scope.realModelChart = createBarPlot($scope, '#realmodelchart', $scope.realmodel);

    }, function(response) {
      alert(response.error)
    });
  
  for (var i = 0; i < 300; i++)
    $scope.usermodel.push(0)  
  
  $scope.usermodel[0] = 0.1;
  $scope.usermodel[1] = -0.2;
  $scope.usermodel[2] = 0.3;
  $scope.usermodel[3] = -0.4;
  $scope.usermodel[4] = 0.5;
  $scope.usermodel[5] = -0.6;
  $scope.usermodel[6] = 0.7;
  $scope.usermodel[7] = -0.8;
  $scope.usermodel[8] = 0.9;
  $scope.usermodel[9] = -1.0;
 
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
  
  console.log("render", dataset)
  
  var extent = d3.max([Math.abs(d3.min(dataset)), d3.max(dataset)]);
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
            console.log("clicked", p)
            dataset[p.y] = p.x;
            console.log("clicked", dataset);
            $('#usermodelchart svg').remove();
            createBarPlot($scope, '#usermodelchart', dataset);
            // render($scope, svg, dataset, width, height);
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
      console.log("rect width", d)
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