AppModule.controller("CreateDeliveryController",[
    "$scope", "$log", "$authentication", "$location",
    function ($scope, $log, $authentication, $location) {
        $scope.pickup = {
            choice : "customer"
        };

        $scope.delivery= {
            choice : "customer"
        };
    }

]);

