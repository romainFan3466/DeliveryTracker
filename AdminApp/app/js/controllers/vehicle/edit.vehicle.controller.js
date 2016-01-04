AppModule.controller("EditVehicleController",[
    "$scope", "$log", "$vehicle",
    function ($scope, $log, $vehicle) {
        
        

        $scope.vehicle = {};
        $scope.vehicles = {};
        $scope.editor = false;
        $scope.found = false;
        var vehicleTemp = {};
        $scope.success = false;
        $scope.retrieved = "";
        $scope.error = {
            value : false,
            info : ""
        };


        var getAllVehicles = function(){
            $vehicle.getAll().then(
                function(res){
                    $scope.vehicles = res.vehicles;
                },
                function(res){
                    $log.log("impossible to load vehicles")
                }
            );
        };

        $scope.onSelect = function(item, model, label){
            $scope.success = false;
            $scope.error.value = false;
            angular.copy(item, $scope.vehicle);
            angular.copy($scope.vehicle, vehicleTemp);
            $scope.found = true;
        };


        $scope.resetChange = function(){
            angular.copy(vehicleTemp, $scope.vehicle);
        };


        $scope.update = function (vehicle) {
            
            var updatedVehicle = {};
            
             angular.forEach($scope.vehicle, function(value,key){
                    if(!angular.equals(value, vehicleTemp[key])){
                        updatedVehicle[key] = value;
                    }
                });
            
            $vehicle.update(vehicle.id, updatedVehicle).then(
                function (res) {
                    $scope.error.value = false;
                    $scope.vehicle = {};
                    $scope.found = false;
                    vehicleTemp = {};
                    $scope.retrieved = "";
                    getAllVehicles();
                    $scope.editor = false;
                    $scope.success = true;
                },
                function (res) {
                    $scope.error.value = true;
                    $scope.error.info = res.info || "no info";
                }
            );
        };
        



        getAllVehicles();


        
    }

]);