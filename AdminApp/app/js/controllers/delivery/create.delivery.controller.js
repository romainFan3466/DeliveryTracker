AppModule.controller("CreateDeliveryController",[
    "$scope", "$log", "$authentication", "$customer","$delivery",
    function ($scope, $log, $authentication, $customer, $delivery) {

        $scope.customers = [];
        $scope.customer = {};


        $scope.details = {
            pickup : {},
            delivery : {}
        };

        $scope.search ={
            customer : "",
            pickup : "",
            delivery : "",
            addressPickup : "",
            addressDelivery : ""
        };

        var _selectedCustomerPickupLocation = {};
        var _selectedCustomerDeliveryLocation = {};




        $scope.delivery ={
            locationPickup : {
                lat : "",
                lng : ""
            },
            locationDelivery : {
                lat : "",
                lng : ""
            },
            dateCreated : "",
            customerId : "",
            info : "",
            weight : "",
            area : "",
            content : ""

        };

        $scope.homeAddress = "";


        $scope.pickup = {
            choice : "customer"
        };

        $scope.delivery= {
            choice : "customer"
        };

        $scope.onSelectCustomer = function(item, model, label){
            $scope.delivery.customerId = item.id;
            angular.copy(item, $scope.customer);
        };

        /*$customer.getAddress(item.location.lat, item.location.lng).then(
            function(res){
                $scope.homeAddress = res.address;
            }
        );*/

        $scope.createDelivery = function(){
            _setPickup();
            _setDelivery();
            $scope.delivery.dateCreated = new Date();
            $delivery.create($scope.delivery).then(
                function(res){

                },
                function(res){

                }
            );
        };




        $scope.onSelectPickup = function(item, model, label){
            _selectedCustomerPickupLocation = item.location;
        };

        $scope.onSelectDelivery = function(item, model, label){
            _selectedCustomerDeliveryLocation = item.location;
        };


        $customer.getAll().then(
            function (res) {
                $scope.customers = res.customers;
            },
            function (res) {
                $log.log("impossible to load customers")
            }
        );

        var _setPickup = function(){
            if($scope.pickupLocation == "address"){
                var l = {
                    lat : $scope.details.pickup.lat,
                    lng : $scope.details.pickup.lng
                };
                $scope.delivery.locationPickup = l;
                //angular.copy($scope.details.pickup.lng, $scope.delivery.locationPickup.lng);
            }
            else if ($scope.pickupLocation == "customer"){
                $scope.delivery.locationPickup = _selectedCustomerPickupLocation;
            }
        };


        var _setDelivery = function(){
            if($scope.deliveryLocation == "address"){
                var l = {
                    lat : $scope.details.delivery.lat,
                    lng : $scope.details.delivery.lng
                };
                $scope.delivery.locationDelivery = l;
            }

            else if ($scope.deliveryLocation == "customer"){
                $scope.delivery.locationDelivery = _selectedCustomerDeliveryLocation;
            }
        };


    }

]);

