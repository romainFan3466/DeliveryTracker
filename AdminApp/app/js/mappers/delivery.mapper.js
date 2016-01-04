AppModule.factory('DeliveryMapper',
    function () {

        var args  = [
            "id",
            "locationPickup",
            "locationDelivery",
            "customerId",
            "dateCreated",
            "weight",
            "area",
            "info",
            "content"
        ];



        var DeliveryMapper = function(data, restrict){
            if(restrict != true){
                for (var k in args){
                    if(args[k] == "locationPickup" || args[k] == "locationDelivery"){
                        this[args[k]] = {
                            lat : "",
                            lng : ""
                        };
                    }
                    else{
                        this[args[k]] = "";
                    }
                }
            }

            if (angular.isDefined(data)) {
                this.parse(data, restrict);
            }
        };

        DeliveryMapper.prototype.parse= function(data, restrict){
            if (data) {
                var self = this;

                    angular.forEach(data, function (value, key) {
                        var _key = humps.camelize(key);

                        if(args.indexOf(_key) != -1){

                            if((_key == "locationPickup" || _key=="locationDelivery")
                                && angular.isDefined(value.lat) && angular.isDefined(value.lng)){
                                self[_key] = {
                                    lat : parseFloat(value.lat),
                                    lng : parseFloat(value.lng)
                                };
                            }

                            //else if(_key == "dateCreated"){
                            //
                            //}
                            else {
                                self[_key] = value;
                            }
                        }
                    });
            }
        };

        return DeliveryMapper;
    }
);