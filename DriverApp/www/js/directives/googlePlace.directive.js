AppModule.directive('googleplace', ["$log", function($log) {
    return {
        require: 'ngModel',
        scope: {
            ngModel: '=',
            details: '=?'
        },
        link: function(scope, element, attrs, model) {

            var components = {
                "locality" : "city",
                "administrative_area_level_1" : "province",
                "country":"country",
                "postal_code" : "zip"
            };

            scope.gPlace = new google.maps.places.Autocomplete(element[0]);

            google.maps.event.addListener(scope.gPlace, 'place_changed', function() {
                var geoComponents = scope.gPlace.getPlace();
                var latitude = geoComponents.geometry.location.lat();
                var longitude = geoComponents.geometry.location.lng();
                var addressComponents = geoComponents.address_components;
                var fields = {};

                for (var i = 0; i < addressComponents.length; i++) {
                        var address = addressComponents[i];
                        if (components[address.types[0]]) {
                            fields[components[address.types[0]]] = address.long_name;
                        }
                }

                fields.lat = latitude.toFixed(6);
                fields.lng = longitude.toFixed(6);

                scope.$apply(function() {
                    scope.details = fields;
                    model.$setViewValue(element.val());
                });
            });
        }
    };
}]);
