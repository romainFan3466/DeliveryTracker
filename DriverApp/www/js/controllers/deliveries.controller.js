AppModule.controller("DeliveriesController", [
    "$scope", "$log","$state",
    function ($scope, $log, $state) {

        $scope.go = function(path){
            $state.go("app.deliveries"+path);
        };

    }]);