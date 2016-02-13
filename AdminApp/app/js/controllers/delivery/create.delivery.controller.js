AppModule.controller("CreateDeliveryController",[
    "$scope", "$log", "$authentication", "$customer","$delivery","$driver",
    function ($scope, $log, $authentication, $customer, $delivery, $driver) {

        $scope.customers = [];
        $scope.customer = {};
        $scope.error = {
            value: false,
            info: ""
        };

        $scope.opened =false;

        $scope.success = false;

        var _init = function () {
            $scope.search = {
                customer: "",
                driver : "",
                pickup: "",
                delivery: ""
            };

            $scope.now = new Date();

            $scope.delivery = {
                senderId : "",
                receiverId : "",
                driverId :"",
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

        var _assign = function (deliveryId, driverId) {
            $delivery.assign(deliveryId, driverId).then(
                function (res) {

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



        $scope.createDelivery = function(){
            $scope.delivery.dateCreated = new Date();

            $delivery.create($scope.delivery).then(
                function(res){
                    if (angular.isDefined($scope.delivery.driverId) &&
                        $scope.delivery.driverId != "") {
                        _assign(res.deliveryId, $scope.delivery.driverId);
                    }
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


        $scope.onSelectCustomer = function (item, model, label) {
            $scope.delivery.customerId = item.id;
            angular.copy(item, $scope.customer);
        };


        $scope.onSelectSender = function(item, model, label){
            $scope.delivery.senderId = item.id;
            //angular.copy(item, $scope.sender);
            $scope.sender = item;
        };


        $scope.onSelectDriver = function (item, model, label) {
            $scope.delivery.driverId= item.id;
            $scope.driver = item;
        };

        $scope.onSelectReceiver = function(item, model, label){
            $scope.delivery.receiverId = item.id;
            //angular.copy(item, $scope.receiver);
            $scope.receiver = item;
        };


        $customer.getAll().then(
            function (res) {
                $scope.customers = res.customers;
            },
            function (res) {
                $log.log("impossible to load customers")
            }
        );

        $driver.getAll().then(
            function (res) {
                $scope.drivers = res.drivers;
            },
            function (res) {
                $log.log("load drivers impossible");
            }
        );

        _init();

    }

]);

