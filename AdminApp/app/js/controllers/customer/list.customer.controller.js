AppModule.controller("ListCustomerController",[
    "$scope", "$log", "$customer","$filter","$uibModal",
    function ($scope, $log, $customer, $filter, $uibModal) {

        var _customers = [];
        $scope.selectedLetter = "";
        $scope.customers = [];
        $scope.alphabet = [];
        $scope.alphabet = $scope.alphabet.concat("ABCDEFGHIJKLMNOPQRSTUVWXYZ".split(""));
        $scope.alphabet.push("0-9");
        $scope.inputSearch="";
        $scope.active = {
            name : false
        };


        $scope.sortArray = function(letter){
            $scope.customers = $filter("firstLetter")(_customers,letter,"name");
            $scope.order("name",false);
            $scope.selectedLetter = letter;
        };

        $scope.$watch('inputSearch', function(value){
            if(angular.isString(value) && !angular.equals(value,"")){
                $scope.customers = $filter("filter")(_customers,value,false);
                $scope.order("name",false);
            }
            else {
                $scope.sortArray($scope.selectedLetter);
                }
            });

        $scope.order = function(predicate, reverse) {
            $scope.customers = $filter('orderBy')($scope.customers, predicate, reverse);
            _setActive(predicate);
        };

        var  _setActive = function(predicate){
            angular.forEach($scope.active,function(value,key){
                $scope.active[key]=(key==predicate);
            });
        };

        $scope.showCustomer = function (customer) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'templates/customer/customerModal.html',
                controller: 'CustomerModalController',
                resolve: {
                    selectedCustomer: function () {
                        return customer;
                    }
                }
            });

            modalInstance.result.then(function () {

            }, function () {

            });
        };


        var _getAllCustomers = function () {
            $customer.getAll().then(
                function (res) {
                    _customers = res.customers;
                    $scope.customers = res.customers;
                    $scope.order("name", false);
                    $log.log($scope.customers);
                }
            );
        };


        _getAllCustomers();




    }

]);
