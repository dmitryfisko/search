app.controller('SearchFieldController', function($http, $window, $state,
    searchResultsService) {
    // debugger
    var self = this;
    var searchString = '';
    var searchResults = [];

    this.keyPress = function(keyEvent) {
        // debugger;
        if (keyEvent.which === 13) {
            self.search();
        }
    }

    this.search = function() {
        var data = {
            q: self.searchString,
            start: 0
        };
        debugger;

        $http.get('/search/', data, null)
        .success(function(response) {
            searchResultsService.initResults(response);
            $state.go('results');
        }
        ).error(function(response) {
            // debugger;
        });
    }
});
