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
