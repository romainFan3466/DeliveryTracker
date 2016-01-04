AppModule.controller("ListVehicleController",[
    "$scope", "$log", "$vehicle","$filter","$uibModal",
    function ($scope, $log, $vehicle, $filter, $uibModal) {

        
        var _vehicles = [];
        $scope.limitBegin = 0;
        $scope.limitEnd = 15;
        $scope.vehicles= [];
        $scope.vehicleName="";

        $scope.active = {
            registration : false
        };


        $scope.bigTotalVehicles=1;

        var _getAllVehicles = function () {
            $vehicle.getAll().then(
                function (result) {
                    _vehicles = result.vehicles;
                    $scope.vehicles=[];
                    $scope.vehicles =result.vehicles;
                    $scope.bigTotalVehicles = result.vehicles.length;
                },
                function (result) {
                    $log.log("error getAll vehicles");
                });
        };



        $scope.$watch('inputSearch', function(value){
           if(angular.isString(value)){
               $scope.vehicles = $filter('filter')(_vehicles, value, false);
               $scope.bigTotalVehicles = $scope.vehicles.length;
           }
        });



        $scope.pageChanged = function(pageNo) {
                $scope.limitEnd= pageNo*15;
                $scope.limitBegin=(pageNo*15)-15;
        };


        $scope.showVehicle = function (vehicle) {

            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'templates/vehicle/vehicleModal.html',
                controller: 'VehicleModalController',
                resolve: {
                    selectedVehicle: function () {
                        return vehicle;
                    }
                }
            });

            modalInstance.result.then(function () {

            }, function () {

            });
        };


        _getAllVehicles();
        
    }

]);
