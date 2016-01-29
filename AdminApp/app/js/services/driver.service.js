AppModule.factory('$driver', [
    "$http", "DriverMapper", "$q", "$log", "Config",
    function ($http, DriverMapper, $q, $log, Config) {


        var _create = function (data) {
            var deferred = $q.defer();
            var driver = new DriverMapper(data);
            $http
                .post(Config.baseUrl + "/drivers", {driver: driver})
                .success(function (res) {
                    deferred.resolve({driverID: res.driverId, password : res.password});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _update = function (id, data) {
            var deferred = $q.defer();
            var driver = new DriverMapper(data, true);
            $http
                .put(Config.baseUrl + "/drivers/" + id, {driver: driver})
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
                .delete(Config.baseUrl + "/drivers/" + id)
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
                .get(Config.baseUrl + "/drivers/" + id)
                .success(function (res) {
                    driver = new DriverMapper(res.driver, true);
                    deferred.resolve({driver: driver});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _getAll = function () {
            var deferred = $q.defer();
            $http
                .get(Config.baseUrl + "/drivers/all")
                .success(function (res) {
                    drivers = [];
                    angular.forEach(res.drivers, function (driver) {
                        c = new DriverMapper(driver.driver, true);
                        drivers.push(c);
                    });
                    deferred.resolve({drivers: drivers});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };





        return {
            create: _create,
            update: _update,
            get: _get,
            getAll: _getAll
        }

    }
]);