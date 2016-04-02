AppModule.controller("DeliveriesProgressController", [
    "$scope", "$log", "$delivery", "$ionicLoading", "$timeout","$filter",
    function ($scope, $log, $delivery, $ionicLoading, $timeout,$filter) {

        var _init = function () {
            $scope.error = {
                value: false,
                info: ""
            };
            $scope.deliveries = [];
        };


        var _getAllFromState = function (state) {
            var d = new Date();
            var start = new Date(d.getFullYear(), d.getMonth(), d.getDate(),0,0,0,0);
            var end = new Date(d.getFullYear(), d.getMonth(), d.getDate(),23,59,59,0);
            cond = {
                start : $filter("date")(start, "yyyy-MM-dd HH:mm:ss"),
                end :$filter("date")(end , "yyyy-MM-dd HH:mm:ss"),
                state : state
            };
            $delivery.getAll(cond).then(
                function (res) {
                    $scope.error.value = false;
                    $scope.deliveries = $scope.deliveries.concat(res.deliveries);
                },
                function (res) {
                    $scope.error = {
                        value: true,
                        info: res.info || ""
                    };
                }
            );
        };


        var _getAll = function () {
            var progress_states = ["taken", "picked up", "on way"];
            $ionicLoading.show();
            angular.forEach(progress_states, _getAllFromState);
            $ionicLoading.hide();
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