AppModule.controller("DeliveriesAllController", [
    "$scope", "$log", "$delivery","$ionicLoading","$timeout","$filter",
    function ($scope, $log, $delivery, $ionicLoading, $timeout, $filter) {

        /*
        TODO : Implement : today date for all getAll
         */

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
                end :$filter("date")(end , "yyyy-MM-dd HH:mm:ss")
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

         $scope.isState = function(status, deliveryState){
            var result = false;

            switch (status){
                case "incoming":
                    result = deliveryState == "not taken";
                    break;
                case "progress":
                    var valid = ["taken", "picked up", "on way"];
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