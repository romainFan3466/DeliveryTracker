AppModule.controller("EditDeliveryController",[
    "$scope", "$log", "$customer", "$delivery","$routeParams","$driver",
    function ($scope, $log, $customer, $delivery, $routeParams, $driver) {


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
        $scope.driver = {};

        $scope.success = false;

        var _init = function () {
            $scope.search = {
                customer :"",
                sender: "",
                receiver: "",
                driver : ""
            };

            $scope.found = false;
            $scope.deliveryId = "";
            $scope.delivery = {
                senderId : "",
                receiverId : "",
                dateCreated: "",
                driverId: "",
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

                if(angular.isDefined(updatedDelivery.driverId)){
                    _assign($scope.delivery.id, updatedDelivery.driverId);
                }

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


        var _assign = function(deliveryId, driverId){
            $driver.assignDelivery(driverId, deliveryId).then(
                function(res){

                },
                function (res) {
                    $scope.error = {
                        value: true,
                        info: res.info
                    };
                    $scope.success = false;
                }
            )
        };


        var initCustomerNames = function () {
            $scope.customer = getCustomer($scope.delivery.customerId);
            $scope.sender = getCustomer($scope.delivery.senderId);
            $scope.receiver= getCustomer($scope.delivery.receiverId);
            $scope.search.customer = $scope.customer.name;
            $scope.search.sender = $scope.sender.name;
            $scope.search.receiver= $scope.receiver.name;
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


        var getDrivers = function(){
            $driver.getAll().then(
                function(res){
                    $scope.drivers = res.drivers;
                    var driverId =$scope.delivery.driverId; 
                    if(angular.isDefined(driverId) && driverId!= null){
                        var driver= getDriver(driverId);
                        $scope.search.driver = driver.name;
                        angular.copy(driver, $scope.driver);
                    }
                },
                function(res){
                    $log.log("load drivers impossible");
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
        
        var getDriver = function (id) {
             var found = null;
             for(var i = 0; i<$scope.drivers.length; i++){
                 if ($scope.drivers[i].id == id){
                     found = true;
                     return $scope.drivers[i];
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
                    getDrivers();
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

        $scope.onSelectCustomer = function (item, model, label) {
            $scope.delivery.customerId= item.id;
            $scope.customer = item;
        };

        $scope.onSelectDriver = function (item, model, label) {
            $scope.delivery.driverId = item.id;
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

        if (angular.isDefined($routeParams.deliveryId)) {
            $scope.deliveryId = $routeParams.deliveryId;
            $scope.getDelivery($routeParams.deliveryId);
        }

    }

]);

