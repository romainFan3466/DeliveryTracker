AppModule.factory('DriverMapper',
    function () {

         var args  = ["id", "name", "email", "phone" , "location", "vehicleId1", "vehicleId2" ];


        var DriverMapper = function(data, restrict){
            if(restrict != true){
                this.id = "";
                this.name = "";
                this.email = "";
                this.phone = "";
                this.location = {
                    lat : "",
                    lng : ""
                };
                this.vehicleId1 = "";
                this.vehicleId2 = "";
            }
            if (angular.isDefined(data)) {
                this.parse(data, restrict);
            }
        };

        DriverMapper.prototype.parse= function(data, restrict){
            if (data) {
                var self = this;
                if(restrict === true){
                    angular.forEach(data, function (value, key) {
                        key = humps.camelize(key);
                        if(args.indexOf(key) != -1){
                            if(key == "location" && angular.isDefined(value.lat) && angular.isDefined(value.lng)){
                                self[key] = {
                                    lat : parseFloat(value.lat),
                                    lng : parseFloat(value.lng)
                                };
                            }
                            else {
                                self[key] = value;
                            }
                        }
                    });
                }
                else{
                    angular.forEach(args, function (key) {
                        if (angular.isDefined(data[key])) {
                            var value = data[key];
                            if (key == "location" && angular.isDefined(value.lat) && angular.isDefined(value.lng)){
                                self[key] = {
                                    lat: parseFloat(value.lat),
                                    lng: parseFloat(value.lng)
                                };
                            }
                        else
                            {
                                self[key] = value;
                            }
                        }
                    });
                }
            }
        };

        return DriverMapper;
    }
);