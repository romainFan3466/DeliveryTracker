AppModule.controller("CreateVehicleController",[
    "$scope", "$log", "$vehicle", "$location",
    function ($scope, $log, $vehicle, $location) {

        var _init = function () {
            $scope.error = {
                value: false,
                info: ""
            };

            $scope.vehicle = {
                registration: "",
                type: "",
                maxWeight: "",
                maxArea: ""
            };
        };

        $scope.success = false;

        $scope.createVehicle = function(vehicle){
            if(!checkAreaAndWeight(vehicle.maxArea, vehicle.maxWeight)){
                $scope.success = false;
                $scope.error.value = true;
                $scope.error.info  = "Area and Weight must be positive number";
            }
            else{
                $vehicle.create(vehicle).then(
                    function(res){
                        _init();
                        $scope.success = true;
                    },
                    function(res) {
                        $scope.success = false;
                        $scope.error.value = true;
                        $scope.error.info  = res.info;
                    }
                );
            }
        };

        var checkAreaAndWeight = function(area, weight){
            var _area = parseFloat(area);
            var _weight = parseFloat(weight);
            return !isNaN(_area) && !isNaN(_weight) && _area>0 && _weight>0

        };

        _init();








    }

]);


