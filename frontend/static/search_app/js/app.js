var app = angular.module('app', ['ui.router']);

app.config(function ($stateProvider, $urlRouterProvider, $httpProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
    .state('index', {
        url: "/",
        templateUrl: "/static/search_app/html/index.html",
        controller: 'SearchFieldController'
    })
    .state('results', {
        url: "/results",
        templateUrl: "/static/search_app/html/results.html",
        controller: 'SearchResultsController'
    });
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.service('searchResultsService', SearchResultsService);
app.service('pagerService', PagerService);

function SearchResultsService() {
    var results = [];

    var getResults = function() {
        return results;
    };

    var initResults = function(data) {
        results = data;
    };

    return {
        getResults: getResults,
        initResults: initResults
    };
}
