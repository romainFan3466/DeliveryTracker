AppModule.controller("DeliveryController", [
    "$scope", "$log", "$delivery", "$ionicLoading", "$stateParams", "$customer", "$ionicModal", "$timeout",
    function ($scope, $log, $delivery, $ionicLoading, $stateParams, $customer, $ionicModal, $timeout) {

        var _init = function () {
            $scope.error = {
                value: false,
                info: ""
            };

            $scope.delivery = {};
            $scope.customer = {};
        };

        $ionicModal.fromTemplateUrl('templates/customer.modal.html', {
            scope: $scope,
            animation: 'slide-in-up'
        }).then(function (modal) {
            $scope.modal = modal
        });

        $scope.open = function (id, title) {
            $scope.titleModal = title;
            _getCustomer(id);
            $scope.modal.show()
        };

        $scope.closeModal = function () {
            $scope.modal.hide();
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