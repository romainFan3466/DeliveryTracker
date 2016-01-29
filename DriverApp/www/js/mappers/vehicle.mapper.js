AppModule.factory('VehicleMapper',
    function () {
        var args = ["id", "registration", "type","area","weight", "maxWeight", "maxArea"];


        var VehicleMapper = function (data, restrict) {
            if (restrict != true) {
                for (var k in args){
                    this[args[k]] = "";
                }

            }
            if (angular.isDefined(data)) {
                this.parse(data, restrict);
            }
        };

        var _parseNumber = function(value){
            var parsed  = parseFloat(value);
            if (isNaN(parsed)){
                return "";
            }
            else {
                return parsed;
            }
        };

        VehicleMapper.prototype.parse = function (data, restrict) {
            if (data) {
                var self = this;

                if (restrict === true) {
                    angular.forEach(data, function (value, key) {
                        if (args.indexOf(key) != -1) {
                            if (key == "maxArea" || key == "maxWeight" ||
                                key == "weight" || key == "area") {
                                    self[key] = _parseNumber(value);
                            }
                            else {
                                self[key] = value;
                            }
                        }
                        else if(key == "max_area"){
                            self.maxArea =  _parseNumber(value);
                        }
                        else if(key == "max_weight"){
                            self.maxWeight = _parseNumber(value);
                        }
                    });
                }
                else {
                    angular.forEach(args, function (key) {
                        if (angular.isDefined(data[key])) {
                            var value = data[key];
                             if (key == "maxArea" || key == "maxWeight" ||
                                key == "weight" || key == "area") {
                                    self[key] = _parseNumber(value);
                            }
                            else {
                                self[key] = value;
                            }
                        }
                    });
                }
            }
        };

        VehicleMapper.prototype.queryFormat = function () {
            if(angular.isDefined(this.maxArea)){
                this.max_area = this.maxArea;
                delete this.maxArea;
            }
            if(angular.isDefined(this.maxWeight)){
                this.max_weight = this.maxWeight;
                delete this.maxWeight;
            }
        };

        return VehicleMapper;

    }
);
