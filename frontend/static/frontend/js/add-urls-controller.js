app.controller('AddUrlsController', function($http) {
    var self = this;

    this.text = '';
    this.depth = 1;

    this.addUrls = function() {
        urls = self.text.split('\n');
        if (urls.length === 0 && urls[0] == "") {
            console.log('error');
            return;
        } else {
            var data = {
                depth: self.depth,
                urls: urls
            }

            var config = {
                headers : {
                    'Content-Type': 'application/json'
                }
            }

            $http.post('api/urls', data, config)
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
