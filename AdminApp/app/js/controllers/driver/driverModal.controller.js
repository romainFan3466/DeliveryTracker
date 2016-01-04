AppModule.controller('DriverModalController',
    function ($scope, $uibModalInstance, selectedDriver, $driver) {

        $scope.driver = selectedDriver;

        //TODO : get info on current driver position and deliveries

        $scope.close = function () {
            $uibModalInstance.close();
        };


});