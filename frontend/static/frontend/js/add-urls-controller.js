app.controller('AddUrlsController', function($http) {
    var self = this;

    this.text = '';
    this.depth = 1;

    this.addUrls = function() {
        urls = self.text.split('\n');
        debugger
        if (urls.length === 0 && urls[0] == "") {
            console.log('error');
            return;
        } else {
            data = {
                depth: self.depth,
                urls: urls
            }

            $http.post('api/urls', data)
            .success(function(response) {
                console.log(response);
            })
            .error(function(response) {
                console.log('vse huevo')
                console.log(response);
            });
        }
    }
});
