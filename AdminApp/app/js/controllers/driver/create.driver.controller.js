AppModule.controller("CreateDriverController",[
    "$scope", "$log", "$driver",
    function ($scope, $log, $driver) {


        var _init = function () {
            $scope.driver = {
                name: "",
                email: "",
                phone: ""
            };

            $scope.error = {
                value: false,
                info: ""
            };

            $scope.password = "";
        };

        $scope.success = false;


        $scope.addDriver = function(driver){
            $driver.create(driver).then(
                function(res){
                   _init();
                    $scope.success = true;
                    $scope.password = res.password;
                },
                function(res){
                    $scope.success = false;
                    $scope.error = {
                        value: true,
                        info : res.info
                    };
                }
            )
        };


        _init();

    }

]);

