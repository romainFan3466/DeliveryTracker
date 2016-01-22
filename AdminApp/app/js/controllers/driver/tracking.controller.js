AppModule.controller('TrackDriverController', [
        "$scope", "$log", "$driver",
        function ($scope, $log, $driver) {
            $scope.readyDriver = false;
            var drivers = [];

            $scope.retrieved = "All";

            $scope.
            $driver.getAll().then(
                function(res){
                    $scope.drivers = res.drivers;
                        angular.copy(res.drivers, drivers);
                        var c = {
                            name: "All"
                        };
                        $scope.drivers.push(c);
                        $scope.markers = getMarkers(drivers);
                        console.log(drivers);
                        $scope.readyDriver = true;
                }
            );
            
            $scope.onSelect = function (item, model, label) {
                if(item.name == "All"){
                    $scope.markers = getMarkers(drivers);
                    console.log(drivers);
                    $scope.readyDriver = true;
                }
                else {
                    $scope.markers = getMarkers([item]);
                    $scope.map = {
                        center: {
                            latitude: item.location.lat,
                            longitude: item.location.lng
                        },
                        zoom: 8
                    };
                    $scope.readyDriver = true;
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
                $scope.driverName = obj.name;
                obj.show = !obj.show;
            };
            $scope.closeClick = function () {
                $scope.windowOptions.visible = false;
            };


        }]
);

//angular.module('appMaps', ['uiGmapgoogle-maps']).controller('mainCtrl', function ($scope) {
//    $scope.map = {center: {latitude: 40.1451, longitude: -99.6680}, zoom: 4, bounds: {}};
//    $scope.options = {scrollwheel: false};
//    var createRandomMarker = function (i, bounds, idKey) {
//        var lat_min = bounds.southwest.latitude, lat_range = bounds.northeast.latitude - lat_min, lng_min = bounds.southwest.longitude, lng_range = bounds.northeast.longitude - lng_min;
//        if (idKey == null) {
//            idKey = "id";
//        }
//        var latitude = lat_min + (Math.random() * lat_range);
//        var longitude = lng_min + (Math.random() * lng_range);
//        var ret = {latitude: latitude, longitude: longitude, title: 'm' + i};
//        ret[idKey] = i;
//        return ret;
//    };
//    $scope.randomMarkers = [];
//    $scope.$watch(function () {
//        return $scope.map.bounds;
//    }, function (nv, ov) {
//        if (!ov.southwest && nv.southwest) {
//            var markers = [];
//            for (var i = 0; i < 50; i++) {
//                markers.push(createRandomMarker(i, $scope.map.bounds))
//            }
//            $scope.randomMarkers = markers;
//        }
//    }, true);
//});
//angular.module('appMaps', ['uiGmapgoogle-maps']).controller('mainCtrl', function ($scope, $log) {
//    $scope.map = {center: {latitude: 40.1451, longitude: -99.6680}, zoom: 4}
//    $scope.options = {scrollwheel: false};
//    $scope.marker = {coords: {latitude: 40.1451, longitude: -99.6680}, show: false, id: 0};
//    $scope.windowOptions = {visible: false};
//    $scope.onClick = function () {
//        $scope.windowOptions.visible = !$scope.windowOptions.visible;
//    };
//    $scope.closeClick = function () {
//        $scope.windowOptions.visible = false;
//    };
//    $scope.title = "Window Title!";
//});

//angular.module('appMaps', ['uiGmapgoogle-maps']).controller('mainCtrl', function ($scope) {
//    $scope.map = {center: {latitude: 40.1451, longitude: -99.6680}, zoom: 4, bounds: {}};
//    $scope.options = {scrollwheel: false};
//    var createRandomMarker = function (i, bounds, idKey) {
//        var lat_min = bounds.southwest.latitude, lat_range = bounds.northeast.latitude - lat_min, lng_min = bounds.southwest.longitude, lng_range = bounds.northeast.longitude - lng_min;
//        if (idKey == null) {
//            idKey = "id";
//        }
//        var latitude = lat_min + (Math.random() * lat_range);
//        var longitude = lng_min + (Math.random() * lng_range);
//        var ret = {latitude: latitude, longitude: longitude, title: 'm' + i, show: false};
//        ret[idKey] = i;
//        return ret;
//    };
//    $scope.onClick = function (marker, eventName, model) {
//        console.log("Clicked!");
//        model.show = !model.show;
//    };
//    $scope.randomMarkers = [];
//    $scope.$watch(function () {
//        return $scope.map.bounds;
//    }, function (nv, ov) {
//        if (!ov.southwest && nv.southwest) {
//            var markers = [];
//            for (var i = 0; i < 50; i++) {
//                markers.push(createRandomMarker(i, $scope.map.bounds))
//            }
//            $scope.randomMarkers = markers;
//        }
//    }, true);
//});