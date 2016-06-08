var app = angular.module('app', ['ui.router']);

app.config(function ($stateProvider, $urlRouterProvider, $httpProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
    .state('index', {
        url: "/",
        templateUrl: "/static/frontend/html/index.html",
        controller: 'SearchFieldController'
    })
    .state('results', {
        url: "/results",
        templateUrl: "/static/frontend/html/results.html",
        controller: 'SearchResultsController'
    })
    .state('add_urls', {
        url: "/add_urls",
        templateUrl: "/static/frontend/html/add_urls.html",
        controller: 'AddUrlsController'
    });
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

// app.service('searchResultsService', SearchResultsService);
app.service('pagerService', PagerService);
app.service('searchService', SearchService);

// function SearchResultsService() {
//     var results = [];
//     var resultsCount = 0;
//     var pageLimit;
//     var query;
//
//     var initService = function(q) {
//         query = q;
//     }
//
//     var getResults = function() {
//         return results;
//     };
//
//     var getCount = function() {
//         return resultsCount;
//     }
//
//     var getPageLimit = function() {
//         return pageLimit;
//     }
//
//     var getQuery = function() {
//         return query;
//     }
//
//     var initResults = function(data) {
//         results = data['results'];
//         resultsCount = data['count'];
//         pageLimit = data['limit'];
//     };
//
//     return {
//         getResults: getResults,
//         getCount: getCount,
//         getPageLimit: getPageLimit,
//         getQuery: getQuery,
//         initResults: initResults,
//         initService: initService
//     };
// }
