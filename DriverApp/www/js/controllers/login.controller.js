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

