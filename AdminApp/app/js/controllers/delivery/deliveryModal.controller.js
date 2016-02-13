AppModule.controller('DeliveryModalController',
    function ($scope, $uibModalInstance, selectedDelivery, $customer, $location, $driver, Config, $log) {

        $scope.delivery = selectedDelivery;
        $scope.sender = {};
        $scope.receiver = {};
        $scope.driver = null;
        //TODO : get info on current delivery position and deliveries


         var initCustomers = function () {
             getCustomer($scope.delivery.senderId, 'customer');
             getCustomer($scope.delivery.senderId, 'sender');
             getCustomer($scope.delivery.receiverId, 'receiver');
             if($scope.delivery.state == 'delivered'){
                 $scope.signatureUrl = Config.baseUrl + "/deliveries/signature/"+$scope.delivery.id;
             }

             if($scope.delivery.driverId !=null){
                 $driver.get($scope.delivery.driverId).then(
                     function(res){
                         $scope.driver = res.driver;
                     },
                     function(res){
                         $log.log("impossible to load driver");
                     }
                 )
             }

             //getDriver($scope.delivery.driverId);
        };


        var getCustomer = function(id, key){
            $customer.get(id).then(
                function(res){
                    $scope[key]= res.customer;
                },
                function(res){
                    $log.log("load customer"+ key +" impossible");
                }
            );
        };

        initCustomers();

        $scope.close = function () {
            $uibModalInstance.close();
        };

        $scope.$on('$routeChangeStart', function () {
            $uibModalInstance.close();
        });

        $scope.goToPosition = function(id){
            $location.path("/drivers/track/"+ id);
        };


        $scope.edit = function (id) {
            $location.path("/deliveries/edit/"+ id);
        };


});