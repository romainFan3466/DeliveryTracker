AppModule.factory('CustomerMapper',
    function () {

        var args  = ["id", "name", "address", "phone" , "location" ];


        var CustomerMapper = function(data, restrict){
            if(restrict != true){
                this.id = "";
                this.name = "";
                this.address = "";
                this.phone = "";
                this.location = {
                    lat : "",
                    lng : ""
                };
            }
            if (angular.isDefined(data)) {
                this.parse(data, restrict);
            }
        };

        CustomerMapper.prototype.parse= function(data, restrict){
            if (data) {
                var self = this;

                if(restrict === true){
                    angular.forEach(data, function (value, key) {
                        if(args.indexOf(key) != -1){
                            if(key == "location" && angular.isDefined(value.lat) && angular.isDefined(value.lng)){
                                self[key] = {
                                    lat : parseFloat(value.lat),
                                    lng : parseFloat(value.lng)
                                };
                            }
                            else if (key == "address"){
                                self[key] = value.replace(',', /\n/g);
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
                            value = data[key];
                            if (key == "location" && angular.isDefined(value.lat) && angular.isDefined(value.lng)){
                                self[key] = {
                                    lat: parseFloat(value.lat),
                                    lng: parseFloat(value.lng)
                                };
                            }
                            else if (key == "address"){
                                self[key] = value.replace(',', '<br>');
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

        return CustomerMapper;
    }
);