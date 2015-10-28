/**
 * Created by romain on 26/10/15.
 */
var AppModule = angular.module('DeliveryTrackerAdmin.app', [
    'ngRoute' ,
    'ngResource',
    'angular.filter']);


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
    baseUrl : "http://",
    TVA : 0.20
});


AppModule.config(['$routeProvider', function ($routeProvider) {
	var routes = [
		{url: "/login", templateUrl: "templates/login.view.html"},
        {url: "/home", templateUrl: "templates/home.template.html"},
        {url: "/settings", templateUrl: "templates/settings.view.html"}
	];

	$routeProvider.otherwise({redirectTo: '/home'});

	angular.forEach(routes, function (route) {

        /*route.resolve = {
            resolve : "$start"
            };*/
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


        var SessionMapper = function (data) {

            /**
             * @ngdoc property
             * @name authenticated
             * @propertyOf appModule.object:SessionMapper
             * @description
             * True if user is authenticated, else false
             * @returns {boolean} identifier
             */
            this.authenticated = false;

            /**
             * @ngdoc property
             * @name uid
             * @propertyOf appModule.object:SessionMapper
             * @description
             * SessionMapper user identifier
             * @returns {string} identifier
             */
            this.uid = "";

            /**
             * @ngdoc property
             * @name email
             * @propertyOf appModule.object:SessionMapper
             * @description
             * SessionMapper user email
             * @returns {string} email
             */
            this.email = "";

            if (angular.isDefined(data)) {
                this.parse(data);
            }
        };

        
        /** @ngdoc method
         * @name parse
         * @methodOf appModule.object:SessionMapper
         * @param {Object} data This object is supposed to have the same propriety than SessionMapper.
         * @description
         * Set all propriety matching by a provided object
         */
        SessionMapper.prototype.parse = function(data){
            if (data) {
                var self = this;
                angular.forEach(data, function (value, key) {
                    self[key] = value;
                });
            }
        };


        return SessionMapper;
    }
);
/**
 * @ngdoc overview
 * @name appModule
 * @description
 *
 * This is where all directives, services are regrouped for the project " Washing App"
 *
 *
 *
 */



/**
 * @ngdoc service
 * @name appModule.service:$authentication
 * @require $http
 * @require SessionMapper
 * @require $q
 * @require Config
 * @description
 * This service provides all authentication functionalities from the API.
 *
 * Using this service, you can manage user session and allows to retrieve data from server.
 */
AppModule.factory('$authentication',[
    "$http", "SessionMapper", "$q", "$log", "Config",
    function ($http, SessionMapper, $q, $log, Config) {


        var _modelSession = {
            authenticated : true
        };

        var _getSession = function(){
            var deferred = $q.defer();

            $http
                .get(Config.baseUrl + '/php/session')
                .success(function (res) {
                    _modelSession = new SessionMapper(res);

                    deferred.resolve( {email : _modelSession.email});
                })
                .error(function(res){
                    deferred.reject(res);
                });

            return deferred.promise;
        };


        var _getUserData = function(){
            var deferred = $q.defer();

            $http
                .post(Config.baseUrl + '/php/session/user', {})
                .success(function (res) {
                    deferred.resolve({user : res.user});
                })
                .error(function(res){
                    deferred.reject({message : res.message});
                });

            return deferred.promise;
        };


        var _loginIn = function (credentials) {
            var deferred = $q.defer();
            var cred = {
                user : credentials
            };

            $http
                .post(Config.baseUrl + '/php/login', cred)
                .success(function (res) {
                    _modelSession = new SessionMapper(res);
                    deferred.resolve( {email : _modelSession.email});
                })
                .error(function(res){
                    deferred.reject({message : res.message});
                });

            return deferred.promise;
        };


        var _logout = function () {
            var deferred = $q.defer();
            $http
                .get(Config.baseUrl + '/php/logout')
                .success(function (res) {
                    _modelSession = new SessionMapper(res);
                    deferred.resolve({message : res.message});
                });

            return deferred.promise;
        };


        var _signUp = function (credentials) {
            var deferred = $q.defer();
            var user = { user : credentials};
            $http
                .post(Config.baseUrl + '/php/signUp', user)
                .success(function (res) {
                    deferred.resolve(res);
                })
                .error(function(res){
                    deferred.reject({message : res.message});
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
            signUp  : _signUp,
            isAuthenticated : _isAuthenticated,
            getUserMail : _getUserMail,
            getSession : _getSession,
            getUserData : _getUserData
        };
    }]
);


/**
 * @ngdoc controller
 * @name appModule.controller:LoginController
 * @require $scope
 * @require $authentication
 * @require $location
 * @require $modal
 *
 * @description
 *
 * Interacts with template : "login.view.html"
 *
 */
AppModule.controller("LoginController",[
    "$scope", "$log", "$modal", "$authentication", "$location",
    function ($scope, $log, $modal, $authentication, $location) {

        $scope.login = {
            email : "",
            password : ""
        };


        $scope.signupCredentials = {
            email:'',
            password:'',
            confirmedPassword:""
        };

        $scope.loading=false;
        $scope.wrongCredentials=false;


        $scope.loginIn = function (credentials) {
            $scope.loading=true;
            $authentication.loginIn(credentials).then(
                function (result) {
                    $scope.loading=false;
                    $location.path("/home");
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


    $scope.openNewUserModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'html/views/newUser.modal.html',
            controller: 'NewUserModalController'
        });

        modalInstance.result.then(
            //result from login modal
            function (info) {

        },
            //fail from login modal
            function () {
            $log.info('Error create user request : ' + new Date());
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