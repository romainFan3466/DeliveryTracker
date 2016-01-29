
AppModule.controller("LoginController",[
    "$scope", "$log", "$authentication", "$location","$timeout",
    function ($scope, $log, $authentication, $location, $timeout) {

        $scope.login = {
            email : "",
            password : "",
            type : "admin"
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

