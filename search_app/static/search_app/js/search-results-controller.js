app.controller('SearchResultsController', function($state, searchResultsService) {
    var self = this;

    this.results = searchResultsService.getResults();
    this.pager = {};
    this.setPage = setPage;

    initController();

    function initController() {
        // initialize to page 1
        self.setPage(1);
        if (searchResultsService.getResults().length === 0) {
            $state.go('index');
        }
    }

    function setPage(page) {
        if (page < 1 || page > self.pager.totalPages) {
            return;
        }

        // get pager object from service
        self.pager = PagerService().getPager(self.results.length, page);

        // get current page of items
        self.pageResults = self.results.slice(self.pager.startIndex, self.pager.endIndex);
    }
});
