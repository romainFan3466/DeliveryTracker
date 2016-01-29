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