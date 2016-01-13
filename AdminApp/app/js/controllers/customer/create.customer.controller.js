AppModule.controller("CreateCustomerController",[
    "$scope", "$log", "$authentication", "$customer",
    function ($scope, $log, $authentication, $customer) {

        $scope.customer = {};
        $scope.success = false;
        $scope.error = false;
        $scope.errorInfo = "";
        $scope.details = null;
        $scope.address = "";

        $scope.$watch("address", function(address){
           if(!angular.isDefined(address)){
               $scope.details = null;
           }
        });

        $scope.addCustomer = function(customer){
            if(!angular.isDefined(customer.address) ||customer.address=="" || $scope.details == null){
                $scope.error = true;
                $scope.success = false;
                $scope.errorInfo= "Missing address";
            }
            else{
                //angular.copy($scope.address, $scope.customer.address);
                $scope.customer.location = {
                    lat : $scope.details.lat,
                    lng : $scope.details.lng
                };

                $customer.create(customer).then(
                    function(res){
                        $scope.customer = {};
                        $scope.success = true;
                        $scope.error = false;
                    },
                    function(res){
                        $scope.error = true;
                        $scope.success = false;
                        $scope.errorInfo = res.info || "no info"
                    }
                )
            }
        };


    }

]);

