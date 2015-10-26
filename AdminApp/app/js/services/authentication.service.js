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

