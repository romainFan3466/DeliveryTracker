AppModule.controller("ListDriverController",[
    "$scope", "$log", "$driver","$filter", "$uibModal",
    function ($scope, $log, $driver, $filter, $uibModal) {

        
        var _drivers = [];
        $scope.selectedLetter = "";
        $scope.drivers = [];
        $scope.alphabet = [];
        $scope.alphabet = $scope.alphabet.concat("ABCDEFGHIJKLMNOPQRSTUVWXYZ".split(""));
        $scope.inputSearch="";
        $scope.active = {
            name : false
        };


        $scope.sortArray = function(letter){
            $scope.drivers = $filter("firstLetter")(_drivers,letter,"name");
            $scope.order("name",false);
            $scope.selectedLetter = letter;
        };

        $scope.$watch('inputSearch', function(value){
            if(angular.isString(value) && !angular.equals(value,"")){
                $scope.drivers = $filter("filter")(_drivers,value,false);
                $scope.order("name",false);
            }
            else {
                $scope.sortArray($scope.selectedLetter);
                }
            });

        $scope.order = function(predicate, reverse) {
            $scope.drivers = $filter('orderBy')($scope.drivers, predicate, reverse);
            _setActive(predicate);
        };

        var  _setActive = function(predicate){
            angular.forEach($scope.active,function(value,key){
                $scope.active[key]=(key==predicate);
            });
        };

        $scope.showDriver = function (driver) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'templates/driver/driverModal.html',
                controller: 'DriverModalController',
                resolve: {
                    selectedDriver: function () {
                        return driver;
                    }
                }
            });

            modalInstance.result.then(function () {

            }, function () {

            });
        };


        var _getAllDrivers = function () {
            $driver.getAll().then(
                function (res) {
                    _drivers = res.drivers;
                    $scope.drivers = res.drivers;
                    $scope.order("name", false);
                    $log.log($scope.drivers);
                }
            );
        };


        _getAllDrivers();

    }

]);


