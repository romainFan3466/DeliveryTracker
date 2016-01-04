AppModule.factory('$vehicle', [
    "$http", "VehicleMapper", "$q", "$log", "Config",
    function ($http, VehicleMapper, $q, $log, Config) {


        var _create = function (data) {
            var deferred = $q.defer();
            var vehicle = new VehicleMapper(data,true);
            vehicle.queryFormat();
            $http
                .post(Config.baseUrl + "/vehicles", {vehicle: vehicle})
                .success(function (res) {
                    deferred.resolve({vehicleID: res.vehicleId});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _update = function (id, data) {
            var deferred = $q.defer();
            var vehicle = new VehicleMapper(data, true);
            vehicle.queryFormat();
            $http
                .put(Config.baseUrl + "/vehicles/" + id, {vehicle: vehicle})
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
                .delete(Config.baseUrl + "/vehicles/" + id)
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
                .get(Config.baseUrl + "/vehicles/" + id)
                .success(function (res) {
                    vehicle = new VehicleMapper(res.vehicle, true);
                    deferred.resolve({vehicle: vehicle});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _getAll = function () {
            var deferred = $q.defer();
            $http
                .get(Config.baseUrl + "/vehicles/all")
                .success(function (res) {
                    vehicles = [];
                    angular.forEach(res.vehicles, function (vehicle) {
                        c = new VehicleMapper(vehicle.vehicle, true);
                        vehicles.push(c);
                    });
                    deferred.resolve({vehicles: vehicles});
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
            getAll : _getAll
        }
    }
]);
