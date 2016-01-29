AppModule.factory('DeliveryMapper', [
    "$filter",
    function ($filter) {

        var args = [
            "id",
            "customerId",
            "customerName",
            "senderId",
            "driverId",
            "receiverId",
            "dateCreated",
            "dateDue",
            "weight",
            "area",
            "info",
            "content"
        ];


        var DeliveryMapper = function (data, restrict) {
            if (restrict != true) {
                for (var k in args) {
                        this[args[k]] = "";
                    }
                }

            if (angular.isDefined(data)) {
                this.parse(data, restrict);
            }
        };


        DeliveryMapper.prototype.parse = function (data, restrict) {
            if (data) {
                var self = this;

                angular.forEach(data, function (value, key) {
                    var _key = humps.camelize(key);

                    if (args.indexOf(_key) != -1) {
                        if(_key == "dateCreated" || _key == "dateDue"){
                            self[_key] = $filter('date')(value, "yyyy-MM-dd HH:mm:ss");
                        }
                        else if(_key == "area" || _key == "weight" ){
                            if(value !=null){
                                self[_key] = parseFloat(value);
                            }
                            else {
                                self[_key] = null;
                            }
                        }
                        else {
                            self[_key] = value;
                        }
                    }
                });
            }
        };

        DeliveryMapper.prototype.queryFormat = function () {
            return humps.decamelizeKeys(this);

        };

        return DeliveryMapper;
    }
]);