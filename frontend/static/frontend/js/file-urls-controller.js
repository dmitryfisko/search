app.controller('FileUrlsController', function($scope, fileUploadService){
    var self = this;

    this.uploadFile = function() {
        var uploadUrl = "/api/urls";
        fileUploadService.uploadFileToUrl(this.urlsFile, uploadUrl);
    };
});
