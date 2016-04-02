AppModule.controller("DeliveriesIncomingController", [
    "$scope", "$log", "$delivery","$ionicLoading","$timeout","$filter",
    function ($scope, $log, $delivery, $ionicLoading, $timeout, $filter) {

         var _init = function () {
            $scope.error = {
                value: false,
                info: ""
            };

            $scope.deliveries = [];
        };


        var _getAll = function () {
            var d = new Date();
            var start = new Date(d.getFullYear(), d.getMonth(), d.getDate(),0,0,0,0);
            var end = new Date(d.getFullYear(), d.getMonth(), d.getDate(),23,59,59,0);
            cond = {
                start : $filter("date")(start, "yyyy-MM-dd HH:mm:ss"),
                end :$filter("date")(end , "yyyy-MM-dd HH:mm:ss"),
                state : "not taken"
            };
            
            $delivery.getAll(cond).then(
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