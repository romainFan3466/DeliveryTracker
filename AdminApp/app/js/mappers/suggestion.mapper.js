AppModule.factory('SuggestionMapper',[
    "DriverMapper", "DeliveryMapper",
    function (DriverMapper, DeliveryMapper) {

        var SuggestionMapper = function(data){
            this.driver = {};
            this.deliveries = [];

            if (angular.isDefined(data)) {
                this.parse(data);
            }
        };

        SuggestionMapper.prototype.parse= function(data){
            if (data) {
                var self = this;
                if (angular.isDefined(data.driver)) {
                    self.driver = new DriverMapper(data.driver);
                }
                if (angular.isDefined(data.deliveries) &&
                    angular.isArray(data.deliveries)) {

                    angular.forEach(data.deliveries, function (d) {
                        self.deliveries.push({"delivery": new DeliveryMapper(d["delivery"]), "distance": d["distance"], "duration": d["duration"]});
                    })
                }
            }
        };

        return SuggestionMapper;
    }



]);