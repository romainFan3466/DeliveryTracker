
var AppModule = angular.module('DeliveryTrackerAdmin.app', [
    'ngRoute' ,
    'ngResource',
    'angular.filter']);

AppModule.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    //$httpProvider.defaults.useXDomain = true;
}]);
/**
 * @ngdoc object
 * @name appModule.object:Config
 *
 * @description
 * Config is a global object regrouping constant variables for the entire app.
 *
 *
 */
AppModule.constant('Config', {
    /**
     * @ngdoc property
     * @name baseUrl
     * @propertyOf appModule.object:Config
     * @description
     * Base Url of the API.
     *
     * The rest of the URL is completed by services, depends of the methods.
     * @returns {String} baseUrl
     */
    baseUrl : "http://127.0.0.1:5000/api"
});

AppModule.run(["$rootScope", "$location", "$authentication","$log",
    function ($rootScope, $location, $authentication, $log) {
        $rootScope.$on("$routeChangeError", function (event, next, current, rejection) {
            //$authentication.getSession().then(
            //    function(result){
            //        var auth = $authentication.isAuthenticated();
            //        if(auth ==false){
            //            event.preventDefault();
            //            $location.path("/login");
            //        }
            //    },
            //
            //    function(result){
            //        event.preventDefault();
            //        $location.path("/login");
            //    }
            //);
            //var auth = $authentication.isAuthenticated();
            //if (auth == false) {
            //    event.preventDefault();
            //    $location.path("/login");
            //}

            $location.path("/login");

        });
    }
]);


AppModule.config(['$routeProvider', function ($routeProvider) {
	var routes = [
		{url: "/login", templateUrl: "templates/login.html", controller:"LoginController"},
        {url: "/home", templateUrl: "templates/home.html"},
        {url: "/settings", templateUrl: "templates/settings.view.html"},

        {url: "/customers/create", templateUrl: "templates/customer/create.customer.html", controller : "CreateCustomerController"},
        {url: "/customers/edit", templateUrl: "templates/customer/edit.customer.html", controller : "EditCustomerController"},
        {url: "/customers/list", templateUrl: "templates/customer/list.customer.html", controller : "ListCustomerController"},
        
        {url: "/vehicles/create", templateUrl: "templates/vehicle/create.vehicle.html", controller : "CreateVehicleController"},
        {url: "/vehicles/edit", templateUrl: "templates/vehicle/edit.vehicle.html", controller : "EditVehicleController"},
        {url: "/vehicles/list", templateUrl: "templates/vehicle/list.vehicle.html", controller : "ListVehicleController"},

        {url: "/deliveries/create", templateUrl: "templates/delivery/create.delivery.html", controller : "CreateDeliveryController"},
        {url: "/deliveries/edit", templateUrl: "templates/delivery/edit.delivery.html", controller : "EditDeliveryController"},
        {url: "/deliveries/list", templateUrl: "templates/delivery/list.delivery.html", controller : "ListDeliveryController"},
        {url: "/deliveries/assign", templateUrl: "templates/delivery/assign.delivery.html", controller : "AssignDeliveryController"},
        
        {url: "/drivers/create", templateUrl: "templates/driver/create.driver.html", controller : "CreateDriverController"},
        {url: "/drivers/edit", templateUrl: "templates/driver/edit.driver.html", controller : "EditDriverController"},
        {url: "/drivers/list", templateUrl: "templates/driver/list.driver.html", controller : "ListDriverController"}
	];

	$routeProvider.otherwise({redirectTo: '/home'});

	angular.forEach(routes, function (route) {
        if(route.url != "/login"){
            route.resolve = {
                sess: function ($authentication) {
                    return $authentication.getSession()
                }
            };
        }
        $routeProvider.when(route.url, route);
	});

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

/**
 * @ngdoc object
 * @name appModule.object:SessionMapper
 *
 * @description
 * This object parses session data into a SessionMapper object
 *
 *
 */
AppModule.factory('SessionMapper',
    function () {


        var SessionMapper = function (data, authenticated) {


            this.authenticated = authenticated;
            this.id = "";
            this.email = "";
            this.companyId = "";
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
                        deferred.resolve( {name : _modelSession.name});
                    }
                    else{
                        _modelSession = new SessionMapper(null, false);
                        deferred.reject();
                    }
                })
                .error(function(res){
                    _modelSession = new SessionMapper(null, false);
                    deferred.reject();
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
                    deferred.resolve( {name : _modelSession.name});
                })
                .error(function(res){
                    var info = (angular.isDefined(res.info))? res.info : null;
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


AppModule.controller("CreateCustomerController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);


AppModule.controller("EditCustomerController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);

AppModule.controller("ListCustomerController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);

AppModule.controller("AssignDeliveryController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);

AppModule.controller("CreateDeliveryController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {
        $scope.pickup = {
            choice : "customer"
        };

        $scope.delivery= {
            choice : "customer"
        };
    }

]);


AppModule.controller("EditDeliveryController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);


AppModule.controller("ListDeliveryController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);


AppModule.controller("CreateDriverController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);



AppModule.controller("EditDriverController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {



    }

]);


AppModule.controller("ListDriverController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);




AppModule.controller("LoginController",[
    "$scope", "$log", "$authentication", "$location","$timeout",
    function ($scope, $log, $authentication, $location, $timeout) {

        $scope.login = {
            email : "",
            password : ""
        };

        $scope.loading=false;
        $scope.wrongCredentials=false;


        $scope.loginIn = function (credentials) {
            $scope.loading=true;
            $authentication.loginIn(credentials).then(
                function (result) {
                    $scope.loading=false;
                    $timeout(
                        function(){
                            $location.path("/home");
                        },
                        2000
                    )

                },
                function(result){
                    $scope.loading=false;
                    $scope.wrongCredentials=true;
                }

            );
        };


        $scope.logout = function () {
            $authentication.logout().then(function (results) {
            });
        };





}]);


/**
 * @ngdoc controller
 * @name appModule.controller:NewUserModalController
 * @require $scope
 * @require $authentication
 * @require $modalInstance
 *
 * @description
 *
 * Interacts with template : "newUser.modal.html"
 *
 */
AppModule.controller('NewUserModalController',[
    "$scope", "$modalInstance","$authentication", "$log",
 function ($scope, $modalInstance, $authentication, $log) {

    $scope.credentials = {
        email : "",
        password : "",
        confirmedPassword:"",
        company : "",
        address : "",
        city : "",
        country :"",
        phone : ""
    };


     $scope.success=false;
     $scope.error=false;
     $scope.differentPassword = false;
     $scope.loading=false;
     $scope.differentPassword=false;



    $scope.$watchCollection('credentials', function(newValue){
        $scope.differentPassword = newValue.confirmedPassword!="" &&
            newValue.password!=""&&
            !angular.equals(newValue.confirmedPassword, newValue.password);
    });


     $scope.signUp = function (credentials) {
         $scope.loading= true;

             $authentication.signUp(credentials).then(
                 function (results) {
                     $scope.loading=false;
                     $scope.success=true;
                 },
                 function(){
                     $scope.loading=false;
                     $scope.error=true;
                 });
     };


    $scope.ok = function () {
        $modalInstance.close("succes");
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);
AppModule.controller("NavBarController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

        $scope.authenticated = false;

        $scope.isAuthenticated = function(){
            var v = $authentication.isAuthenticated();
            $log.log(v)
        };

        $scope.$watch($authentication.isAuthenticated, function(value){
            $scope.authenticated = value;
        });

        $scope.login = function(){
            $location.path("/login")
        };

        $scope.logout = function(){
            $authentication.logout().then(
                function(){
                    $location.path("/login")
                },
                function(){
                    $location.path("/login")
                }
            )
        };
    }

]);

AppModule.controller("CreateVehicleController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);



AppModule.controller("EditVehicleController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);
AppModule.controller("ListVehicleController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {

    }

]);
