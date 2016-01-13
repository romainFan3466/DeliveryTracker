AppModule.controller("EditDeliveryController",[
    "$scope", "$log", "$customer", "$delivery",
    function ($scope, $log, $customer, $delivery) {


        var customers = [];
        $scope.customer = {};
        $scope.error = {
            value: false,
            info: ""
        };

        $scope.errorSearch = {
            value: false,
            info: ""
        };

        var deliveryTemp = {};

        $scope.editor = false;

        $scope.sender = {};
        $scope.receiver = {};

        $scope.success = false;

        var _init = function () {
            $scope.search = {
                sender: "",
                receiver: ""
            };

            $scope.found = false;
            $scope.deliveryId = "";
            $scope.delivery = {
                senderId : "",
                receiverId : "",
                dateCreated: "",
                customerId: "",
                info: "",
                weight: "",
                area: "",
                content: ""

            };
            $scope.homeAddress = "";
        };


        $scope.update = function (delivery) {
            if(!angular.isDefined(delivery.senderId) || delivery.senderId == ""
                || !angular.isDefined(delivery.receiverId) || delivery.receiverId ==""){
                $scope.error = true;
                $scope.success = false;
                $scope.errorInfo = "Missing sender or receiver";
            }
            else {
                var updatedDelivery = {};
                angular.forEach($scope.delivery, function (value, key) {
                    if (!angular.equals(value, deliveryTemp[key])) {
                        updatedDelivery[key] = value;
                    }
                });

                $delivery.update($scope.delivery.id, updatedDelivery).then(
                    function(res){
                        $scope.success = true;
                        $scope.error.value = false;
                        _init();
                        deliveryTemp = {};
                        $scope.editor = false;
                    },
                    function (res) {
                        $scope.error = {
                            value: true,
                            info: res.info
                        };
                        $scope.success = false;
                    }
                );
            }

        };


        var initCustomerNames = function () {
            $scope.sender = getCustomer($scope.delivery.senderId);
            $scope.receiver= getCustomer($scope.delivery.receiverId);
            $scope.search = {
                sender: $scope.sender.name,
                receiver: $scope.receiver.name
            };
        };


        var getCustomers = function(){
            $customer.getAll().then(
                function(res){
                    $scope.customers = res.customers;
                    initCustomerNames();
                },
                function(res){
                    $log.log("load customers impossible");
                }
            );
        };

         var getCustomer = function (id) {
             var found = null;
             for(var i = 0; i<$scope.customers.length; i++){
                 if ($scope.customers[i].id == id){
                     found = true;
                     return $scope.customers[i];
                 }
             }
             if (found != true) {
                 return null;
             }
         };


        $scope.getDelivery = function(id){
            $delivery.get(id).then(
                function(res){
                    $scope.found = true;
                    angular.copy(res.delivery, $scope.delivery);
                    angular.copy(res.delivery, deliveryTemp);
                    getCustomers();
                    $scope.editor = false;
                    $scope.errorSearch.value = false;
                },
                function(res){
                    $scope.found = false;
                    $scope.errorSearch = {
                        value : true,
                        info: res.info
                    };
                }
            );
        };


        $scope.onSelectSender = function (item, model, label) {
            $scope.delivery.senderId = item.id;
            $scope.sender = item;
        };

        $scope.onSelectReceiver = function (item, model, label) {
            $scope.delivery.receiverId = item.id;
            $scope.receiver = item;
        };


         $scope.resetChange = function(){
             angular.copy(deliveryTemp, $scope.delivery);
             initCustomerNames();
        };

        _init();

    }

]);

