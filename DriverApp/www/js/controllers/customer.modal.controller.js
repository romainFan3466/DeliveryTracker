AppModule.controller('CustomerModalController', [
    "$scope", "$ionicModal", "$customer","$stateParams","$ionicLoading",
    function ($scope, $ionicModal, $customer, $stateParams, $ionicLoading) {

        $scope.customer = {};

        var _getCustomer = function(id){
            $ionicLoading.show();
            $customer.get(id).then(
                function(res){
                    $scope.customer = res.customer;
                    $ionicLoading.hide();
                },
                function(res){
                    $ionicLoading.hide();
                }
            );
        };
    }
]);
