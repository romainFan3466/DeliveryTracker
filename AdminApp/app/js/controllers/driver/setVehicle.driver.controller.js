AppModule.controller("SetVehicleController",[
    "$scope", "$log", "$driver", "$vehicle",
    function ($scope, $log, $driver, $vehicle) {

        $scope.found = false;
        $scope.success = false;
        $scope.drivers = {};
        $scope.vehicles = {};

        var _init = function () {
            $scope.driver = {};
            $scope.retrieved = "";
            $scope.vehicle1 = null;
            $scope.vehicle2 = null;
            $scope.v1 = "";
            $scope.v2 = "";
            $scope.error = {
                value: false,
                info: ""
            };
        };

         var getAllVehicles = function(){
            $vehicle.getAll().then(
                function(res){
                    $scope.vehicles = res.vehicles;
                    vNone = {
                        id : "None"
                    };
                    $scope.vehicles.push(vNone);
                },
                function(res){
                    $log.log("impossible to load vehicles")
                }
            );
        };

        var getAllDrivers = function(){
            $driver.getAll().then(
                function(res){
                    $scope.drivers = res.drivers;
                },
                function(res){
                    $log.log("impossible to load drivers")
                }
            );
        };


        $scope.onSelect = function (item, model, label) {
            $scope.found = true;
            $scope.error.value = false;
            $scope.driver = angular.copy(item);
            $scope.found = true;
        };


        $scope.onSelectVehicle = function (item, model, label, vehicle) {
            $scope.error.value = false;
            $scope[vehicle] = angular.copy(item);
            $scope[vehicle].id = (item.id == "None")? null : item.id;

        };



        $scope.setVehicle = function(driverId, v1Id, v2Id){
            $driver.setVehicle(driverId, v1Id, v2Id).then(
                function(res){
                    $scope.error.value = false;
                    $scope.success = true;
                    _init()
                },
                function(res){
                    $scope.error = {
                        value: true,
                        info: res.info || ""
                    };
                }
            )
        };



        _init();

        getAllDrivers();

        getAllVehicles();



    }

]);

