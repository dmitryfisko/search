app.directive('inputUrl', function() {
    var self = this;
    this.textarea = null;
    this.text = '';

    return {
        link: function(scope, elem, attrs) {
            self.textarea = elem.find('textarea')[0];
            textarea.onkeypress = function(event) {
                if (event.which === 13) {
                    console.log('jsdajfsaj');
                    console.log(self.textarea)
                }
            }
        }
    }
})
