AppModule.controller("EditCustomerController",[
    "$scope", "$log", "$customer", "$location",
    function ($scope, $log, $customer, $location) {

        $scope.customers = {};
        $scope.editor = false;
        $scope.found = false;
        var customerTemp = {};
        $scope.updated = false;
        $scope.details = null;
        var addressTemp = "";

        var getAllCustomers = function(){
            $customer.getAll().then(
                function(res){
                    $scope.customers = res.customers;
                },
                function(res){
                    $log.log("impossible to load customers")
                }
            );
        };

        $scope.onSelect = function(item, model, label){
            $scope.updated = false;
            $scope.customer = item;
            if(item.location && item.location.lat && item.location.lng){
                getAddress(item);
            }
            else{
                angular.copy($scope.customer, customerTemp);
                angular.copy($scope.customer.location, $scope.details);
                $scope.found = true;
            }
        };

        var getAddress = function(item){
            $customer.getAddress(item.location.lat,item.location.lng).then(
                function(res){
                    $scope.address = res.address;
                    addressTemp = res.address;
                    angular.copy($scope.customer, customerTemp);
                    angular.copy($scope.customer.location, $scope.details);
                    $scope.found = true;
                }
            );
        };

        $scope.resetChange = function(){
            angular.copy(customerTemp, $scope.customer);
        };


        $scope.update = function (customer) {
            if (!angular.isDefined($scope.address)|| ($scope.address!= addressTemp && $scope.details==null)) {
                $scope.error = true;
                $scope.success = false;
                $scope.errorInfo = "Missing address";
            }
            else {
                updatedCustomer = {};

                if($scope.details!=null){
                    $scope.customer.location = {
                        lat: $scope.details.lat,
                        lng: $scope.details.lng
                    };
                }

                angular.forEach($scope.customer, function(value,key){
                    if(!angular.equals(value, customerTemp[key])){
                        updatedCustomer[key] = value;
                    }
                });

                updateCustomer(customer.id, updatedCustomer);
            }

        };

        $scope.$watch("address", function(address){
           if(!angular.isDefined(address)){
               $scope.details = null;
           }
        });


        var updateCustomer = function(id, customer){
            $customer.update(id, customer).then(
                    function(res){
                        $scope.error = false;
                        $scope.customer = {};
                        $scope.found = false;
                        customerTemp = {};
                        $scope.updated = true;
                        $scope.address = "";
                        $scope.retrieved = "";
                        getAllCustomers();
                        $scope.editor = false;
                    },
                    function(res){
                        $scope.error = true;
                        $scope.errorInfo = res.info || "no info";
                    }
                );
        };

        getAllCustomers();



    }

]);
