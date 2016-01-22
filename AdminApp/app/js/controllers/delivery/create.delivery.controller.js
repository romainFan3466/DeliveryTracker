AppModule.controller("CreateDeliveryController",[
    "$scope", "$log", "$authentication", "$customer","$delivery",
    function ($scope, $log, $authentication, $customer, $delivery) {

        $scope.customers = [];
        $scope.customer = {};
        $scope.error = {
            value: false,
            info: ""
        };

        $scope.opened =false;

        $scope.success = false;

        var _selectedCustomerPickupLocation = {};
        var _selectedCustomerDeliveryLocation = {};


        var _init = function () {
            $scope.search = {
                customer: "",
                pickup: "",
                delivery: ""
            };

            $scope.now = new Date();

            $scope.delivery = {
                senderId : "",
                receiverId : "",
                dateCreated: "",
                dateDue : "",
                customerId: "",
                info: "",
                weight: "",
                area: "",
                content: ""

            };
            $scope.homeAddress = "";
        };


        $scope.onSelectCustomer = function(item, model, label){
            $scope.delivery.customerId = item.id;
            angular.copy(item, $scope.customer);
        };


        $scope.createDelivery = function(){
            $scope.delivery.dateCreated = new Date();
            $delivery.create($scope.delivery).then(
                function(res){
                    _init();
                    $scope.error.value = false;
                    $scope.success = true;
                },
                function(res){
                    $scope.success =false;
                    $scope.error ={
                        value : true,
                        info : res.info
                    };
                }
            );
        };

        $scope.open = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.opened = !$scope.opened;
        };

        $scope.onSelectSender = function(item, model, label){
            $scope.delivery.senderId = item.id;
            //angular.copy(item, $scope.sender);
            $scope.sender = item;
        };

        $scope.onSelectReceiver = function(item, model, label){
            $scope.delivery.receiverId = item.id;
            //angular.copy(item, $scope.receiver);
            $scope.receiver = item;
        };


        var getCustomer = function (id) {
            angular.forEach($scope.customers, function (c) {
                if (c.id == id) {
                    return c;
                }
            });
            return null;
        };


        $customer.getAll().then(
            function (res) {
                $scope.customers = res.customers;
            },
            function (res) {
                $log.log("impossible to load customers")
            }
        );

        _init();

    }

]);

