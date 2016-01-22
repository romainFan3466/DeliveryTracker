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
            angular.copy($scope.customer, customerTemp);
            $scope.customer.address = item.address.replace(/<br>/g, ',');
            angular.copy($scope.customer.location, $scope.details);
            $scope.found = true;

        };


        $scope.resetChange = function(){
            angular.copy(customerTemp, $scope.customer);
        };


        $scope.update = function (customer) {
            if (!angular.isDefined(customer.address)|| ($scope.customer!= customerTemp.address && $scope.details==null)) {
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

        $scope.$watch("customer.address", function(address){
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
