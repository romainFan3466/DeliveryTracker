AppModule.controller("DeliveryController", [
    "$scope", "$log", "$delivery", "$ionicLoading", "$stateParams", "$customer", "$ionicModal", "$timeout","$window","$ionicPopup",
    function ($scope, $log, $delivery, $ionicLoading, $stateParams, $customer, $ionicModal, $timeout, $window, $ionicPopup) {

        var _init = function () {
            $scope.error = {
                value: false,
                info: ""
            };

            $scope.delivery = {};
            $scope.customer = {};
        };



        $scope.isBalanced= function(status, deliveryState){

            if(!angular.isDefined(deliveryState)){
                return false;
            }

            var result = false;
            var valid = [];
            switch (status){
                case "taken":
                    result = deliveryState !="not taken";
                    break;
                case "picked up":
                    valid = ["picked up", "on way", "delivered"];
                    result = valid.indexOf(deliveryState)!=-1;
                    break;
                case "on way":
                    valid = ["delivered"];
                    result = deliveryState == "delivered";
                    break;
                case "delivered":
                    result = deliveryState == "delivered";
                    break;
                default :
            }
            return result;
        };

        $scope.showState = function(status, deliveryState){
            if (!angular.isDefined(deliveryState)) {
                return false;
            }

            var result = false;
            var valid = [];
            switch (status){
                case "taken":
                        result = true;
                    break;
                case "picked up":
                    result = deliveryState != "not taken";
                    break;
                case "on way":
                    valid = ["on way", "delivered"];
                    result = valid.indexOf(deliveryState)!=-1;
                    break;
                case "delivered":
                    valid = ["delivered"];
                    result = valid.indexOf(deliveryState)!=-1;
                    break;
                default :
            }
            return result;
        };


        $ionicModal.fromTemplateUrl('templates/customer.modal.html', {
            id : 1,
            scope: $scope,
            animation: 'slide-in-up'
        }).then(function (modal) {
            $scope.modal = modal
        });


        $ionicModal.fromTemplateUrl('templates/signature.html', {
            id : 2,
            scope: $scope,
            animation: 'slide-in-up'
        }).then(function (modal) {
            $scope.modal2 = modal
        });


        $scope.showCancel = function () {
            var confirmPopup = $ionicPopup.confirm({
                title: 'Confirmation',
                template: 'Are you sure you want to cancel this delivery ?'
            });
            confirmPopup.then(function (res) {
                if (res) {
                    $scope.setState($scope.delivery.id,"canceled");
                } else {
                    console.log('You are not sure');
                }
            });
        };


        $scope.openCustomer = function (id, title) {
            $scope.titleModal = title;
            _getCustomer(id);
            $scope.modal.show()
        };


        $scope.openSignature = function () {
            $scope.modal2.show()
        };


        $scope.closeModal = function (index) {
            if (index == 1) $scope.modal.hide();
            if (index == 2) $scope.modal2.hide();
        };


        $scope.$on('$destroy', function () {
            $scope.modal.remove();
        });


        var _getCustomer = function (id) {
            $customer.get(id).then(
                function (res) {
                    $scope.customer = res.customer;
                },
                function (res) {
                }
            );
        };


        $scope.setState = function(deliveryId, state){
            $delivery.setState(deliveryId,state).then(
                function(){
                    $scope.closeModal(2);
                    $ionicLoading.show();
                    $scope.getDelivery(deliveryId);
                },
                function(){

                }

            )
        };


        $scope.getDelivery = function (id) {
            $delivery.get(id)
                .then(
                function (res) {
                    $scope.error.value = false;
                    $scope.delivery = res.delivery;
                    $ionicLoading.hide();
                },
                function (res) {
                    $scope.error = {
                        value: true,
                        info: res.info || ""
                    };
                    $ionicLoading.hide();
                }
            )
                .finally(function () {
                    $scope.$broadcast('scroll.refreshComplete');
                });
        };

        $scope.uploadPOD = function(deliveryId, file){
            $delivery.uploadPOD(deliveryId, file).then(
                function(res){
                    $log.log("uploaded");
                    $scope.setState(deliveryId, "delivered");
                },
                function(res){
                    $log.log("error");
                }
            )
        };


        $scope.$on('$ionicView.enter', function () {
            _init();
            if (angular.isDefined($stateParams.deliveryId)) {
                $ionicLoading.show();
                $timeout(
                    function () {
                        $scope.getDelivery($stateParams.deliveryId);
                    },
                    1000
                );
            }
        });

    }
]);