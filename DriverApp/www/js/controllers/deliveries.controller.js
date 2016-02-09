AppModule.controller("DeliveriesController", [
    "$scope", "$log","$state","$cordovaBarcodeScanner", "$ionicPlatform",
    function ($scope, $log, $state, $cordovaBarcodeScanner, $ionicPlatform) {

        $scope.go = function(path){
            $state.go("app.deliveries"+path);
        };

         $ionicPlatform.ready(function () {
             $scope.scanCode = function () {
                 $cordovaBarcodeScanner
                     .scan()
                     .then(function (barcodeData) {
                         $state.go("app.single", {deliveryId : barcodeData.text})
                     }, function (error) {
                         alert("barecode not recognized");
                     });
             };
         });

        //#app/deliveries/id/{{delivery.id}}

    }]);