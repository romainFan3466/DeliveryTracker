
AppModule.controller("EditDriverController",[
    "$scope", "$log", "$driver",
    function ($scope, $log, $driver) {

        

        $scope.editor = false;
        $scope.found = false;
        $scope.success = {
            edited : false,
            deleted : false
        };
        var driverTemp = {};

        var _init = function () {
            $scope.driver = {};
            $scope.drivers = {};
            driverTemp = {};
            $scope.retrieved = "";
            $scope.error = {
                value: false,
                info: ""
            };
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
            $scope.success = {
                edited: false,
                deleted: false
            };
            $scope.error.value = false;
            angular.copy(item, $scope.driver);
            angular.copy($scope.driver, driverTemp);
            $scope.found = true;
        };


        $scope.resetChange = function(){
            angular.copy(driverTemp, $scope.driver);
        };


        $scope.update = function (driver) {
            
            var updatedDriver = {};
            
             angular.forEach($scope.driver, function(value,key){
                    if(!angular.equals(value, driverTemp[key])){
                        updatedDriver[key] = value;
                    }
                });
            
            $driver.update(driver.id, updatedDriver).then(
                function (res) {
                    _init();
                    $scope.found = false;
                    getAllDrivers();
                    $scope.editor = false;
                    $scope.success.edited = true;
                },
                function (res) {
                    $scope.error.value = true;
                    $scope.error.info = res.info || "no info";
                }
            );
        };
        


        _init();

        getAllDrivers();




    }

]);

