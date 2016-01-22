AppModule.controller("ListDeliveryController", [
    "$scope", "$log", "$authentication", "$location",

    function ($scope, $log, $authentication, $location) {

        $scope.openedTo = false;
        $scope.openedFrom = false;
        $scope.formats = 'dd-MMMM-yyyy';
        $scope.dateOptions = {
            startingDay: 1
        };


        $scope.open = function ($event, string) {
            $event.preventDefault();
            $event.stopPropagation();

            if (string == "to") {
                $scope.openedTo = true;
                $scope.openedFrom = false;
            }
            else if (string == "from") {
                $scope.openedTo = false;
                $scope.openedFrom = true;
            }
        };


    }
]);
