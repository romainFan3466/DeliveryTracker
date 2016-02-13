
var AppModule = angular.module('DeliveryTrackerMobile.app', [
    'ionic',
    'ngCordova',
    'signature'
]);

AppModule.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    //$httpProvider.defaults.useXDomain = true;
}]);

//AppModule.config(function($compileProvider ){
//  $compileProvider.aHrefSanitizationWhitelist(/^\s*(geo):/);
//});


AppModule.run(["$rootScope", "$ionicPlatform", "$state", "$log", "$cordovaDialogs", "$ionicHistory", "$interval",
    function ($rootScope, $ionicPlatform, $state, $log, $cordovaDialogs, $ionicHistory, $interval) {
        $rootScope.positionInterval = null;
        $rootScope.uploadCount = 0;

        function onRequestSuccess(success) {
        }

        function onRequestFailure(error) {
            console.error("Accuracy request failed: error code= " + error);
            if (error.code !== cordova.plugins.locationAccuracy.ERROR_USER_DISAGREED) {
                if (window.confirm("Failed to automatically set Location Mode to 'High Accuracy'. Would you like to switch to the Location Settings page and do this manually?")) {
                    cordova.plugins.diagnostic.switchToLocationSettings();
                }
            }
            else {
                navigator.app.exitApp();
            }
        }

        $rootScope.$on('$stateChangeError',
            function (event, toState, toParams, fromState, fromParams, error) {
                $state.go("app.login");
            });


        $rootScope.$on('$stateChangeSuccess',
            function (event, toState, toParams, fromState, fromParams, error) {
                if (toState.name && toState.name != "app.login" && toState.name != "app.debug" && toState.name != "app") {
                    if ($rootScope.positionInterval == null) {
                        $rootScope.positionInterval = $interval(function () {
                            $rootScope.uploadCount++;
                            $rootScope.$broadcast('upload-counter');
                            $log.log("update positon...");
                        }, 5000);
                    }
                }
            });


        $ionicPlatform.ready(function () {
            // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
            // for form inputs)
            if (window.cordova && window.cordova.plugins.Keyboard) {
                cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
                cordova.plugins.Keyboard.disableScroll(true);

            }
            if (window.StatusBar) {
                // org.apache.cordova.statusbar required
                StatusBar.styleDefault();
            }

            $ionicPlatform.registerBackButtonAction(function () {
                if ($ionicHistory.backView() != null) {
                    $ionicHistory.goBack();
                }
                else {
                    $cordovaDialogs.confirm('Leave ?', '', ['No', 'Yes'])
                        .then(function (buttonIndex) {
                            // no button = 0, 'OK' = 1, 'Cancel' = 2
                            if (buttonIndex == 2) {
                                navigator.app.exitApp();
                            }
                        }
                    );
                }
            }, 100);

            if (window.cordova) {
                cordova.plugins.locationAccuracy.request(onRequestSuccess, onRequestFailure, cordova.plugins.locationAccuracy.REQUEST_PRIORITY_HIGH_ACCURACY);

                cordova.plugins.backgroundMode.setDefaults({
                            title: 'LocationProcess',
                            text: 'Executing background locations.'
                        });

                cordova.plugins.backgroundMode.enable();

                cordova.plugins.backgroundMode.onactivate = function () {
                    setTimeout(function () {
                        cordova.plugins.backgroundMode.configure({
                            text: 'Live tracking running'
                        });
                    }, 2000);
                };

                cordova.plugins.backgroundMode.ondeactivate = function () {};
            }
        });
    }
]);
AppModule.constant('Config', {
    baseUrl : "http://deliverytracker.romainfanara.com/api"
    //baseUrl : "http://127.0.0.1:5000/api"
});

AppModule.directive('googleplace', ["$log", function($log) {
    return {
        require: 'ngModel',
        scope: {
            ngModel: '=',
            details: '=?'
        },
        link: function(scope, element, attrs, model) {

            var components = {
                "locality" : "city",
                "administrative_area_level_1" : "province",
                "country":"country",
                "postal_code" : "zip"
            };

            scope.gPlace = new google.maps.places.Autocomplete(element[0]);

            google.maps.event.addListener(scope.gPlace, 'place_changed', function() {
                var geoComponents = scope.gPlace.getPlace();
                var latitude = geoComponents.geometry.location.lat();
                var longitude = geoComponents.geometry.location.lng();
                var addressComponents = geoComponents.address_components;
                var fields = {};

                for (var i = 0; i < addressComponents.length; i++) {
                        var address = addressComponents[i];
                        if (components[address.types[0]]) {
                            fields[components[address.types[0]]] = address.long_name;
                        }
                }

                fields.lat = latitude.toFixed(6);
                fields.lng = longitude.toFixed(6);

                scope.$apply(function() {
                    scope.details = fields;
                    model.$setViewValue(element.val());
                });
            });
        }
    };
}]);

/**
 * @ngdoc directive
 * @name appModule.directive:ngGo
 * @element ANY
 * @restrict A

 @param {expression} ngGo  Path expression to evaluate and go to it

 * @description
 * When you click on the current element, you will be redirected to the provided path
 */
AppModule.directive("ngGo", function ($location) {
    return {
        restrict  : "A",
        scope     : {
        },
        link : function (scope, element, attrs) {

            element.on('mouseover',function(){
                element.css("cursor","pointer");
            });

            element.on('click',function(){
                scope.$apply($location.path(attrs.ngGo));
            });
        }
    }
});

/**
 * @ngdoc directive
 * @name appModule.directive:spinner
 * @element ANY
 * @restrict E
 * @param {expression} loading  Allow to show/hide the directive
 *
 * @description
 * This directive allows to display a loading spinner.
 *
 * You must provide an expression to evaluate by the attribute **loading**
 *
 *
 */
AppModule.directive("spinner", function () {
    return {
        restrict  : "E",
        scope     : {
            loading: "="
        },
        replace : true,
        template : '<div class="spinner-global  ng-cloak" ng-cloak ng-show="loading">' +
        '<div class ="spinner-img fa fa-refresh fa-spin fa-5x"></div>' +
        '</div>'
    }
});

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
                                self[key] = value.replace(/,/g, '<br>');
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
                                self[key] = value.replace(/,/g, '<br>');
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
            "content",
            "state",
            "canceled"
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
AppModule.factory('DriverMapper',
    function () {

         var args  = ["id", "name", "email", "phone" , "location" ];


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

AppModule.factory('SessionMapper',
    function () {


        var SessionMapper = function (data, authenticated) {


            this.authenticated = authenticated;
            this.id = "";
            this.email = "";
            this.companyId = "";
            this.name = "";
            this.type = "";
            if (angular.isDefined(data)) {
                this.parse(data);
            }
        };

        SessionMapper.prototype.parse = function(data){
            if (data) {
                var self = this;
                angular.forEach(data, function (value, key) {
                    if(key == "company_id"){
                        self.companyId = value;
                    }
                    else {
                        self[key] = value;
                    }

                });
            }
        };


        return SessionMapper;
    }
);
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


AppModule.factory('$authentication',[
    "$http", "SessionMapper", "$q", "$log", "Config",
    function ($http, SessionMapper, $q, $log, Config) {

        var _modelSession = {
            authenticated : false
        };

        var _getSession = function(){
            var deferred = $q.defer();

            $http
                .get(Config.baseUrl + '/status')
                .success(function (res) {
                    if(angular.isDefined(res.session) && res.session != "logout"){
                        _modelSession = new SessionMapper(res.session, true);
                        deferred.resolve( {session : _modelSession});
                    }
                    else{
                        _modelSession = new SessionMapper(null, false);
                        deferred.reject(res);
                    }
                })
                .error(function(res){
                    _modelSession = new SessionMapper(null, false);
                    deferred.reject(res);
                });
            return deferred.promise;
        };


        var _loginIn = function (credentials) {
            var deferred = $q.defer();
            var cred = {
                user : credentials
            };
            $http
                .post(Config.baseUrl + '/signIn', cred)
                .success(function (res) {
                    _modelSession = new SessionMapper(res.session, true);
                    deferred.resolve( {session : _modelSession});
                })
                .error(function(res){
                    var info = (res && res.info)? res.info : null;
                    deferred.reject({info : info});
                });
            return deferred.promise;
        };


        var _logout = function () {
            var deferred = $q.defer();
            $http
                .get(Config.baseUrl + '/logOut')
                .success(function (res) {
                    _modelSession = new SessionMapper(null, false);
                    deferred.resolve({info : res.info});
                })
                .error(function(res){
                    _modelSession = new SessionMapper(null, false);
                    deferred.resolve({info : res.info});
                    });
            return deferred.promise;
        };


        var _isAuthenticated = function () {
            return _modelSession.authenticated;
        };



        var _getUserMail = function(){
            return _modelSession.email;
        };

        return {
            loginIn : _loginIn,
            logout  : _logout,
            isAuthenticated : _isAuthenticated,
            getUserMail : _getUserMail,
            getSession : _getSession
        };
    }]
);


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
AppModule.factory('$delivery',[
    "$http", "DeliveryMapper", "$q", "$log", "Config",
    function ($http, DeliveryMapper, $q, $log, Config) {

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


        function dataURItoBlob(dataURI) {
            var binary = atob(dataURI.split(',')[1]);
            var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
            var array = [];
            for (var i = 0; i < binary.length; i++) {
                array.push(binary.charCodeAt(i));
            }
            return new Blob([new Uint8Array(array)], {
                type: mimeString
            });
        }

        var _uploadPOD = function(deliveryId, file){
            var deferred = $q.defer();
            var fd = new FormData();
            var imgBlob = dataURItoBlob(file);
            fd.append('file', imgBlob);
            $http
                .post(Config.baseUrl + "/deliveries/signature/"+deliveryId,
                fd,
                {
                    transformRequest: angular.identity,
                    headers: {'Content-Type': undefined }
                })
                .success(function (res) {
                    deferred.resolve();
                })
                .error(function (res) {
                    deferred.reject(res);
                });
            return deferred.promise
        };

        var _setState = function(deliveryId, state){
            var deferred = $q.defer();
            $http
                .put(Config.baseUrl + "/deliveries/state", {state : state, delivery_id:deliveryId})
                .success(function (res) {
                    deferred.resolve();
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
            uploadPOD: _uploadPOD,
            setState: _setState
        }
    }
]);
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


        var _assignDelivery = function(driverId, deliveryId){
            var deferred = $q.defer();
            $http
                .put(Config.baseUrl + "/drivers/" + driverId + "/deliveries/" + deliveryId)
                .success(function (res) {
                    deferred.resolve();
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
            getAll: _getAll,
            assignDelivery : _assignDelivery
        }

    }
]);
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

AppModule.controller('CustomerModalController', [
    "$scope", "$ionicModal", "$customer","$stateParams","$ionicLoading",
    function ($scope, $ionicModal, $customer, $stateParams, $ionicLoading) {

        $scope.customer = {};

        var _getCustomer = function(id){
            $ionicLoading.show();
            $customer.get(id).then(
                function(res){
                    $scope.customer = res.customer;
                    $ionicLoading.hide();
                },
                function(res){
                    $ionicLoading.hide();
                }
            );
        };
    }
]);

AppModule.controller("DebugController", [
    "$scope", "$log", "$cordovaGeolocation", "$interval", "$ionicPlatform","$rootScope","$cordovaBarcodeScanner","$window",
    function ($scope, $log, $cordovaGeolocation, $interval, $ionicPlatform, $rootScope, $cordovaBarcodeScanner, $window) {

        $scope.location = {};
        $scope.err = {};
        $scope.info = "I don't know";
        $scope.fired = 0;
        $scope.firedBackground = 0;
        var positionInterval = {};
        $scope.myHeight = 0;
        $scope.myWidth = 0;


        var startWatcher = function () {
            $scope.fired++;
            var watchOptions = {
                timeout: 5000,
                enableHighAccuracy: true // may cause errors if true
            };
            var watch = $cordovaGeolocation.watchPosition(watchOptions);

            watch.then(
                null,
                function (err) {
                    $scope.err = err;
                },
                function (position) {
                    console.log("fires");
                    $scope.fired++;
                    $scope.location.lat = position.coords.latitude;
                    $scope.location.lng = position.coords.longitude;
                });
        };

        $scope.$on('upload-counter', function(){
           $scope.firedBackground = $rootScope.uploadCount;
        });


        $ionicPlatform.ready(function () {
            $scope.getPosition = function () {
                var posOptions = {timeout: 3000, enableHighAccuracy: true};
                $cordovaGeolocation
                    .getCurrentPosition(posOptions)
                    .then(function (position) {
                        $scope.fired++;
                        $scope.location.lat = position.coords.latitude;
                        $scope.location.lng = position.coords.longitude;
                    }, function (err) {
                        $scope.err = err;
                    });
            };

            if(window.cordova){
                $interval(function () {
                    cordova.plugins.diagnostic.isLocationEnabled(function (enabled) {
                        $scope.locationEnable = enabled;
                    }, function (error) {
                        $scope.err = error;
                    });
                }, 1000);
            }

        });




    }]);

AppModule.controller("DeliveriesAllController", [
    "$scope", "$log", "$delivery","$ionicLoading","$timeout",
    function ($scope, $log, $delivery, $ionicLoading, $timeout) {

        var _init = function () {
            $scope.error = {
                value: false,
                info: ""
            };

            $scope.deliveries = [];
        };


        var _getAll = function () {
            $delivery.getAll().then(
                function (res) {
                    $scope.error.value = false;
                    $scope.deliveries = res.deliveries;
                    $ionicLoading.hide();
                },
                function (res) {
                    $ionicLoading.hide();
                    $scope.error = {
                        value: true,
                        info: res.info || ""
                    };
                }
            )
        };

         $scope.isState = function(status, deliveryState){
            var result = false;

            switch (status){
                case "incoming":
                    result = deliveryState == "not taken";
                    break;
                case "progress":
                    valid = ["taken", "picked up", "on way"];
                    result = valid.indexOf(deliveryState)!=-1;
                    break;
                case "delivered":
                    result = deliveryState == "delivered";
                    break;
                default :
            }
            return result;
        };

        $scope.$on('$ionicView.enter', function () {
            _init();
            $ionicLoading.show();
            $timeout(
                function () {
                    _getAll();
                },
                1000
            );
        });

    }
]);
AppModule.controller("DeliveriesController", [
    "$scope", "$log","$state","$cordovaBarcodeScanner", "$ionicPlatform",
    function ($scope, $log, $state, $cordovaBarcodeScanner, $ionicPlatform) {

        $scope.go = function(path){
            $state.go("app.deliveries"+path);
        };

         $ionicPlatform.ready(function () {
             $scope.scanCode = function () {
                 $cordovaBarcodeScanner
                     .scan()
                     .then(function (barcodeData) {
                         $state.go("app.single", {deliveryId : barcodeData.text})
                     }, function (error) {
                         alert("barecode not recognized");
                     });
             };
         });

        //#app/deliveries/id/{{delivery.id}}

    }]);
AppModule.controller("DeliveriesIncomingController", [
    "$scope", "$log", "$delivery","$ionicLoading",
    function ($scope, $log, $delivery, $ionicLoading) {
        
    }
]);
AppModule.controller("DeliveriesProgressController", [
    "$scope", "$log", "$delivery","$ionicLoading",
    function ($scope, $log, $delivery, $ionicLoading) {

    }
]);
AppModule.controller("DeliveryController", [
    "$scope", "$log", "$delivery", "$ionicLoading", "$stateParams", "$customer", "$ionicModal", "$timeout","$window","$ionicPopup",
    function ($scope, $log, $delivery, $ionicLoading, $stateParams, $customer, $ionicModal, $timeout, $window, $ionicPopup) {

        var _init = function () {
            $scope.error = {
                value: false,
                info: ""
            };

            $scope.delivery = {};
            $scope.customer = {};
        };



        $scope.isBalanced= function(status, deliveryState){

            if(!angular.isDefined(deliveryState)){
                return false;
            }

            var result = false;
            var valid = [];
            switch (status){
                case "taken":
                    result = deliveryState !="not taken";
                    break;
                case "picked up":
                    valid = ["picked up", "on way", "delivered"];
                    result = valid.indexOf(deliveryState)!=-1;
                    break;
                case "on way":
                    valid = ["delivered"];
                    result = deliveryState == "delivered";
                    break;
                case "delivered":
                    result = deliveryState == "delivered";
                    break;
                default :
            }
            return result;
        };

        $scope.showState = function(status, deliveryState){
            if (!angular.isDefined(deliveryState)) {
                return false;
            }

            var result = false;
            var valid = [];
            switch (status){
                case "taken":
                        result = true;
                    break;
                case "picked up":
                    result = deliveryState != "not taken";
                    break;
                case "on way":
                    valid = ["on way", "delivered"];
                    result = valid.indexOf(deliveryState)!=-1;
                    break;
                case "delivered":
                    valid = ["delivered"];
                    result = valid.indexOf(deliveryState)!=-1;
                    break;
                default :
            }
            return result;
        };


        $ionicModal.fromTemplateUrl('templates/customer.modal.html', {
            id : 1,
            scope: $scope,
            animation: 'slide-in-up'
        }).then(function (modal) {
            $scope.modal = modal
        });


        $ionicModal.fromTemplateUrl('templates/signature.html', {
            id : 2,
            scope: $scope,
            animation: 'slide-in-up'
        }).then(function (modal) {
            $scope.modal2 = modal
        });


        $scope.showCancel = function () {
            var confirmPopup = $ionicPopup.confirm({
                title: 'Confirmation',
                template: 'Are you sure you want to cancel this delivery ?'
            });
            confirmPopup.then(function (res) {
                if (res) {
                    $scope.setState($scope.delivery.id,"canceled");
                } else {
                    console.log('You are not sure');
                }
            });
        };


        $scope.openCustomer = function (id, title) {
            $scope.titleModal = title;
            _getCustomer(id);
            $scope.modal.show()
        };


        $scope.openSignature = function () {
            $scope.modal2.show()
        };


        $scope.closeModal = function (index) {
            if (index == 1) $scope.modal.hide();
            if (index == 2) $scope.modal2.hide();
        };


        $scope.$on('$destroy', function () {
            $scope.modal.remove();
        });


        var _getCustomer = function (id) {
            $customer.get(id).then(
                function (res) {
                    $scope.customer = res.customer;
                },
                function (res) {
                }
            );
        };


        $scope.setState = function(deliveryId, state){
            $delivery.setState(deliveryId,state).then(
                function(){
                    $scope.closeModal(2);
                    $ionicLoading.show();
                    $scope.getDelivery(deliveryId);
                },
                function(){

                }

            )
        };


        $scope.getDelivery = function (id) {
            $delivery.get(id)
                .then(
                function (res) {
                    $scope.error.value = false;
                    $scope.delivery = res.delivery;
                    $ionicLoading.hide();
                },
                function (res) {
                    $scope.error = {
                        value: true,
                        info: res.info || ""
                    };
                    $ionicLoading.hide();
                }
            )
                .finally(function () {
                    $scope.$broadcast('scroll.refreshComplete');
                });
        };

        $scope.uploadPOD = function(deliveryId, file){
            $delivery.uploadPOD(deliveryId, file).then(
                function(res){
                    $log.log("uploaded");
                    $scope.setState(deliveryId, "delivered");
                },
                function(res){
                    $log.log("error");
                }
            )
        };


        $scope.$on('$ionicView.enter', function () {
            _init();
            if (angular.isDefined($stateParams.deliveryId)) {
                $ionicLoading.show();
                $timeout(
                    function () {
                        $scope.getDelivery($stateParams.deliveryId);
                    },
                    1000
                );
            }
        });

    }
]);
AppModule.controller("LoginController",[
    "$scope", "$log", "$authentication", "$state","$timeout","$ionicHistory","$ionicLoading","$rootScope","$interval",
    function ($scope, $log, $authentication, $state, $timeout, $ionicHistory,$ionicLoading, $rootScope,$interval) {

        $scope.login = {
            email : "driverA@truck.ie",
            password : "czxq4g2s",
            type : "driver"
        };

        $scope.error = {
            value : false,
            info : ""
        };


        $scope.loginIn = function (credentials) {
            $scope.error.value = false;
            $ionicLoading.show();
            $authentication.loginIn(credentials).then(
                function (result) {
                    $timeout(
                        function(){
                            $rootScope.positionInterval = $interval(function(){
                                $rootScope.uploadCount++;
                                 $rootScope.$broadcast('upload-counter');
                                 $log.log("update positon...");
                             }, 5000);
                            $ionicLoading.hide();
                            $ionicHistory.nextViewOptions({historyRoot: true});
                            $state.go("app.deliveries");
                        },
                        2000
                    );
                },
                function(result){
                     $ionicLoading.hide();
                    $scope.error = {
                        value: true,
                        info: (angular.isDefined(result.info))? result.info : ""
                    };
                }
            );
        };


        var isLogged = function(){
            $authentication.getSession().then(
                function(res){
                    $scope.isLogged = true;
                    $scope.session = res.session;
                },
                function(res){
                    $scope.isLogged = false;
                }
            )
        };


        $scope.logout = function () {
            $authentication.logout().then(function (results) {
                $interval.cancel($rootScope.positionInterval);
                isLogged();
            });
        };


        $scope.goDeb = function () {
            $ionicHistory.nextViewOptions({historyRoot: true});
            $state.go("app.deliveries");
        };

        //positionInterval = $interval(function () {
        //        $scope.firedBackground++;
        //    }, 5000);

        //$timeout(function () {
        //            cordova.plugins.notification.local.schedule({
        //                id: 1,
        //                //title: "Production Jour fixe",
        //                text: "New Delivery",
        //                data: {deliveryId: "3"}
        //            });
        //
        //            cordova.plugins.notification.local.on("click", function (notification) {
        //
        //            });
        //        }, 5000);

        $scope.$on('$ionicView.enter', function () {
            isLogged();
            $log.log("fired");
        });

}]);


AppModule.filter('firstLetter', function () {
    return function (input, letter, prop) {

        input = input || [];
        var out = [];

        if (letter==="0-9") {
            input.forEach(function (item) {
                var itembis = (prop)? item[prop]: item;
                if (/^\d.*/.test(itembis)) {
                    out.push(item);
                }
            });
        }
        else{
            input.forEach(function (item) {
                var itembis = (prop)? item[prop]: item;
                if (itembis.charAt(0).toUpperCase() == letter) {
                    out.push(item);
                }
            });
        }

        return out;
    }
});



AppModule.filter('slice', function() {
    return function(input, limit, begin) {
        if (Math.abs(parseInt(limit)) === Infinity) {
            limit = parseInt(limit);
        } else {
            limit = parseInt(limit);
        }
        if (isNaN(limit)) return input;
        if (angular.isNumber(input)) input = input.toString();
        if (!angular.isArray(input) && !angular.isString(input)) return input;

        begin = (!begin || isNaN(begin)) ? 0 : parseInt(begin);
        begin = (begin < 0 && begin >= -input.length) ? input.length + begin : begin;

        if (limit >= 0) {
            return input.slice(begin, limit);
        } else {
            if (begin === 0) {
                return input.slice(limit, input.length);
            } else {
                return input.slice(Math.max(0, begin + limit), begin);
            }
        }
    };
});



AppModule.config(["$stateProvider", "$urlRouterProvider",
    function ($stateProvider, $urlRouterProvider) {

        var states = [
            {
                state: "app",
                route: {
                    url: '/app',
                    abstract: true,
                    templateUrl: 'templates/menu.html'
                }
            },
            {
                state: "app.deliveries",
                route: {
                    url: '/deliveries',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/deliveries.html',
                            controller: "DeliveriesController"
                        }
                    }
                }
            },
            {
                state: "app.deliveriesAll",
                route: {
                    url: '/deliveries/all',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/all.deliveries.html',
                            controller : "DeliveriesAllController"
                        }
                    }
                }
            },
            {
                state: "app.deliveriesProgress",
                route: {
                    url: '/deliveries/progress',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/progress.deliveries.html'
                        }
                    }
                }
            },
            {
                state: "app.deliveriesIncoming",
                route: {
                    url: '/deliveries/incoming',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/incoming.deliveries.html'
                        }
                    }
                }
            },
            {
                state: "app.single",
                route: {
                    url: '/deliveries/id/:deliveryId',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/delivery.html',
                            controller : "DeliveryController"
                        }
                    }
                }
            },
            {
                state: "app.login",
                route: {
                    url: '/login',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/login.html',
                            controller : "LoginController"
                        }
                    }
                }
            },
             {
                state: "app.debug",
                route: {
                    url: '/debug',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/debug.html',
                            controller : "DebugController"
                        }
                    }
                }
            }


        ];

        angular.forEach(states, function (state) {
            if (state.state != "app.login" && state.state != "app.debug" && state.state != "app") {
                state.route.resolve = {
                    sess: function ($authentication) {
                        return $authentication.getSession();
                    }
                };
            }
            $stateProvider.state(state.state, state.route);
        });


        // if none of the above states are matched, use this as the fallback
        $urlRouterProvider.otherwise('/app/deliveries');
    }
]);