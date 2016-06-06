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
        var data ={
            searchString: self.searchString
        };
        // debugger;

        $http.post('/search', data, null)
        .success(function(response) {
            searchResultsService.initResults(response);
            $state.go('results');
        }
        ).error(function(response) {
            // debugger;
        });
    }
});
