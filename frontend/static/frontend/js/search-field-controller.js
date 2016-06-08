app.controller('SearchFieldController', function($http, $window, $state,
    $stateParams, searchService) {
    // debugger

    var self = this;
    this.searchString = searchService.getQuery();
    this.search = function() {
        if (self.searchString.length === 0) {
            return;
        }
        searchService.initService(self.searchString);
        $state.transitionTo('results', $stateParams, {
            reload: true,
            inherit: false,
            notify: true
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
