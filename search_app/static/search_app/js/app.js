var app = angular.module('app', ['ui.router']);

app.config(function ($stateProvider, $urlRouterProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
    .state('index', {
        url: "/",
        templateUrl: "/static/search_app/html/index.html"
    })
    .state('results', {
        url: "/results",
        templateUrl: "/static/search_app/html/results.html"
    });
})

app.controller('SearchController', function($http, $window, $state) {
    var self = this;
    var searchString = '';
    var searchResults = [];
    
    this.search = function() {
        var data ={
            searchString: self.searchString
        };
        // debugger;
            
        $http.post('/search', data, null)
        .success(function(response) {
            // debugger;
            console.log(response);
            self.searchResults = response;
            $state.go('results');
        }
        ).error(function(response) {
            // debugger;
        });
    }
});