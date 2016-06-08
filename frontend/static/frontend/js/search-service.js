function SearchService($q, $http) {
    var query = '';

    var initService = function(q) {
        query = q;
    }

    var getResults = function(page) {
        var defer = $q.defer();
        $http.get('/api/search?q=' + query + '&' + 'start=' + page)
        .success(function(response) {
            defer.resolve(response);
        })
        .error(function(response) {
            console.log('vse huevo')
        });
        console.log(defer.promise);
        return defer.promise;
    }

    return {
        initService: initService,
        getResults: getResults
    };
}
