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