AppModule.controller('TrackCustomerController', [
        "$scope", "$log", "$customer",
        function ($scope, $log, $customer) {
        $scope.readyCustomer = false;

            $scope.markers = {};

            $scope.retrieved = "All";

            var customers = [];

            var getAllCustomers = function () {
                $customer.getAll().then(
                    function (res) {
                        $scope.customers = res.customers;
                        angular.copy(res.customers, customers);
                        var c = {
                            name: "All"
                        };
                        $scope.customers.push(c);
                        $scope.markers = getMarkers(customers);
                        console.log(customers);
                        $scope.readyCustomer = true;
                    },
                    function (res) {
                        $log.log("impossible to load customers")
                    }
                );
            };


            $scope.onSelect = function (item, model, label) {
                if(item.name == "All"){
                    $scope.markers = getMarkers(customers);
                    console.log(customers);
                    $scope.readyCustomer = true;
                }
                else {
                    $scope.markers = getMarkers([item]);
                    $scope.map = {
                        center: {
                            latitude: item.location.lat,
                            longitude: item.location.lng
                        },
                        zoom: 9
                    };
                    $scope.readyCustomer = true;
                }
            };

            var getMarkers =  function(items){
                markers = [];
                angular.forEach(items, function(item){
                    m = {
                        coords: {
                            latitude: item.location.lat,
                            longitude: item.location.lng
                        },
                        name: item.name,
                        id : item.id
                    };
                    markers.push(m);
                });
                return markers;
            };

            $scope.map = {
                center: {
                    latitude: 53.347800,
                    longitude: -6.259700
                },
                zoom: 7
            };

            $scope.options = {
                scrollwheel: true,
                streetViewControl: false
            };



            $scope.windowOptions = {
                visible: false
            };
            $scope.onClick = function (marker, event, obj) {
                $scope.windowOptions.visible = !$scope.windowOptions.visible;
                $scope.customerName = obj.name;
                obj.show = !obj.show;
            };
            $scope.closeClick = function () {
                $scope.windowOptions.visible = false;
            };


            getAllCustomers();

        }]
);
