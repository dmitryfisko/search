app.controller('SearchFieldController', function($http, $window, $state,
    searchResultsService) {
    // debugger
    var self = this;
    var searchString = '';
    this.search = function() {
        var data = {
            q: self.searchString,
            start: 0
        };

        $http.get('/search?q=' + self.searchString + '&' + 'start=0').success(function(response) {
            console.log('zbs')
                searchResultsService.initResults(response['response']['results']);
                $state.go('results');
            }
        ).error(function(response) {
            console.log('vse huevo')
        });

    }

    var searchResults = [];

    this.keyPress = function(keyEvent) {
        // debugger;
        if (keyEvent.which === 13) {
            self.search();
        }
    }
});
