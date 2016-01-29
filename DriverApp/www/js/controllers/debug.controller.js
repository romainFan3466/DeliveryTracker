AppModule.controller("DebugController", [
    "$scope", "$log", "$cordovaGeolocation", "$interval", "$ionicPlatform","$rootScope",
    function ($scope, $log, $cordovaGeolocation, $interval, $ionicPlatform, $rootScope) {

        $scope.location = {};
        $scope.err = {};
        $scope.info = "I don't know";
        $scope.fired = 0;
        $scope.firedBackground = 0;
        var positionInterval = {};


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
