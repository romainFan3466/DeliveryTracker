AppModule.controller("SuggestAssignmentController",[
    "$scope", "$log", "$delivery","$driver","$uibModal",
    function ($scope, $log, $delivery, $driver, $uibModal) {


        $scope.opened =false;


        $scope.loading = false;
        $scope.dateSearch= new Date();

        $scope.now = new Date();

        var init = function () {
            $scope.success = false;
            $scope.suggestions = [];
            $scope.found = false;
            $scope.error = {
                value: false,
                info: ""
            };

        };

        $scope.open = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.opened = !$scope.opened;
        };


        $scope.suggest = function(){
            init();

            $scope.loading = true;
            $delivery.suggest().then(
                function(res){
                    $scope.suggestions =res.suggestions;
                    $scope.found = true;
                    $log.log(res);
                    $scope.loading = false;
                },
                function(res) {
                    $scope.loading = false;
                }
            );
        };


        $scope.showDelivery = function(delivery){
            var modalInstance = $uibModal.open({
                animation: true,
                size : "lg",
                templateUrl: 'templates/delivery/deliveryModal.html',
                controller: 'DeliveryModalController',
                resolve: {
                    selectedDelivery: function () {
                        return delivery;
                    }
                }
            });

            modalInstance.result.then(function () {

            }, function () {

            });
        };


        var assign_one = function (deliveryId, driverId) {
            $delivery.assign(deliveryId, driverId).then(
                function (res) {

                },
                function (res) {
                    $scope.error.value = true;
                    $scope.error.info+=res.info;
                    $scope.success = false;
                }
            )
        };


        $scope.assign = function(suggestions){
            angular.forEach(suggestions, function(suggestion){
                angular.forEach(suggestion.deliveries, function(delivery){
                    assign_one(delivery.delivery.id, suggestion.driver.id)
                })
            });

            $scope.success = $scope.error.value == false;


        };

        init();

    }
]);