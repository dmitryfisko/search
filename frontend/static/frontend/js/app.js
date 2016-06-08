var app = angular.module('app', ['ui.router']);

// app.config(["$locationProvider", function() {
//   $locationProvider.html5Mode(true);
// }]);

app.config(function ($stateProvider, $urlRouterProvider, $httpProvider, $locationProvider) {
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
    $locationProvider.html5Mode(true);
});

app.service('pagerService', PagerService);
app.service('searchService', SearchService);
