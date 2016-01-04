AppModule.controller('CustomerModalController',
    function ($scope, $uibModalInstance, selectedCustomer, $customer) {

        $scope.customer = {};

        $customer.getAddress(selectedCustomer.location.lat, selectedCustomer.location.lng).then(
            function(res){
                $scope.customer = selectedCustomer;
                $scope.customer.address = res.address;
            }
        );

        $scope.close = function () {
            $uibModalInstance.close();
        };


});