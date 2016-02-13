
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

