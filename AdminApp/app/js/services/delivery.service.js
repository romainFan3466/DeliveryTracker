AppModule.factory('$delivery',[
    "$http", "DeliveryMapper", "$q", "$log", "Config","SuggestionMapper",
    function ($http, DeliveryMapper, $q, $log, Config, SuggestionMapper) {

        var _create = function (data) {
            var deferred = $q.defer();
            var delivery = new DeliveryMapper(data, true);
            delivery = delivery.queryFormat();
            $http
                .post(Config.baseUrl + "/deliveries", {delivery: delivery})
                .success(function (res) {
                    deferred.resolve({deliveryId: res.deliveryId});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _update = function (id, data) {
            var deferred = $q.defer();
            var delivery = new DeliveryMapper(data, true);
            delivery = delivery.queryFormat();
            $http
                .put(Config.baseUrl + "/deliveries/" + id , {delivery: delivery})
                .success(function (res) {
                    deferred.resolve();
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _delete = function (id) {
            var deferred = $q.defer();
            $http
                .delete(Config.baseUrl + "/deliveries/" + id)
                .success(function (res) {
                    deferred.resolve();
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _get = function (id) {
            var deferred = $q.defer();
            $http
                .get(Config.baseUrl + "/deliveries/" + id)
                .success(function (res) {
                    delivery = new DeliveryMapper(res.delivery);
                    deferred.resolve({delivery : delivery});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _getAll = function (conditions) {
            var deferred = $q.defer();
            $http
                .post(Config.baseUrl + "/deliveries/all", {conditions : conditions})
                .success(function (res) {
                    deliveries = [];
                    angular.forEach(res.deliveries, function(delivery){
                        c = humps.camelizeKeys(delivery.delivery);
                        c = new DeliveryMapper(c);
                        deliveries.push(c);
                    });
                    deferred.resolve({deliveries: deliveries});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _assign = function(deliveryId, driverId){
            var deferred = $q.defer();
            $http
                .put(Config.baseUrl + "/deliveries/" + deliveryId + "/drivers/" + driverId)
                .success(function (res) {
                    deferred.resolve();
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise

        };


        var _suggest = function(){
            var deferred = $q.defer();
            $http
                .post(Config.baseUrl + "/assignment", {})
                .success(function (res) {
                    result  = [];
                    if(angular.isDefined(res.suggestions)){
                        angular.forEach(res.suggestions, function(suggestion){
                            result.push(new SuggestionMapper(suggestion))
                        })
                    }
                    deferred.resolve({suggestions:result});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise

        };

        return {
            create : _create,
            update : _update,
            get : _get,
            getAll : _getAll,
            assign : _assign,
            suggest : _suggest
        }
    }
]);