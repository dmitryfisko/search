app.controller('SearchFieldController', function($http, $window, $state, searchService) {
    // debugger
    var self = this;
    this.searchString = '';
    this.search = function() {
        searchService.initService(self.searchString);
        $state.go('results');
    }

    var searchResults = [];

    this.keyPress = function(keyEvent) {
        // debugger;
        if (keyEvent.which === 13) {
            self.search();
        }
    }
});
