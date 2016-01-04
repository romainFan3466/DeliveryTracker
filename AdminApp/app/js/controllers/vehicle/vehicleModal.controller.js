AppModule.controller('VehicleModalController',
    function ($scope, $uibModalInstance, selectedVehicle) {

        $scope.vehicle = selectedVehicle;

        //TODO : retrieve who drive the vehicle

        $scope.close = function () {
            $uibModalInstance.close();
        };




});