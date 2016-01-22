AppModule.controller('CustomerModalController',
    function ($scope, $uibModalInstance, selectedCustomer, $customer) {

        $scope.customer = selectedCustomer;

        $scope.customer.address = selectedCustomer.address.replace(/<br>/g, ',');

        $scope.close = function () {
            $uibModalInstance.close();
        };


});