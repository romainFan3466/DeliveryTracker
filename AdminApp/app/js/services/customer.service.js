AppModule.factory('$customer',[
    "$http", "CustomerMapper", "$q", "$log", "Config",
    function ($http, CustomerMapper, $q, $log, Config) {

        var _create = function(data){
            var deferred = $q.defer();
            var customer = new CustomerMapper(data);
            $http
                .post(Config.baseUrl + "/customers", {customer : customer})
                .success(function(res){
                    deferred.resolve({customerID : res.customerId});
                })
                .error(function(res){
                 deferred.reject(res);
                });
            return deferred.promise
        };


        var _update = function (id, data) {
            var deferred = $q.defer();
            var customer = new CustomerMapper(data, true);
            $http
                .put(Config.baseUrl + "/customers/" + id , {customer: customer})
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
                .delete(Config.baseUrl + "/customers/" + id)
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
                .get(Config.baseUrl + "/customers/" + id)
                .success(function (res) {
                    customer = new CustomerMapper(res.customer);
                    deferred.resolve({customer : customer});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };


        var _getAll = function () {
            var deferred = $q.defer();
            $http
                .get(Config.baseUrl + "/customers/all")
                .success(function (res) {
                    customers = [];
                    angular.forEach(res.customers, function(customer){
                        c = new CustomerMapper(customer.customer);
                        customers.push(c);
                    });
                    deferred.resolve({customers: customers});
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };

        var _getAddress = function(lat,lng){
            var deferred = $q.defer();
            var geocoder = new google.maps.Geocoder;
            var loc = {
                location : {
                    lat : lat,
                    lng : lng
                }
            };
            geocoder.geocode(loc, function(res){
                deferred.resolve({address : res[0].formatted_address});
            });
            return deferred.promise;
        };


        return {
            create : _create,
            update : _update,
            get : _get,
            getAll : _getAll,
            getAddress : _getAddress
        }
    }
]);