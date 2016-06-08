app.controller('SearchResultsController', function($http, searchService) {
    var self = this;

    this.results = [];
    this.pager = {};
    this.setPage = setPage;
    this.loadingState = false;

    initController();

    function initController() {
        // initialize to page 1
        self.setPage(1);
        // if (searchResultsService.getCount() === 0) {
        //     $state.go('index');
        // }
    }

    function setPage(page) {
        if (page < 1 || page > self.pager.totalPages) {
            return;
        }

        self.loadingState = true;
        response = searchService.getResults(page - 1).then(function(data) {
            response = data['response'];
            console.log(response);
            self.results = response['results'];
            self.pager = PagerService().getPager(response['count'],
                page, response['limit']);
            self.loadingState = false;

        });
    }
});
