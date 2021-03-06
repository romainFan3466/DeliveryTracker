
AppModule.config(['$routeProvider', function ($routeProvider) {
	var routes = [
		{url: "/login", templateUrl: "templates/login.html", controller:"LoginController"},
        {url: "/home", templateUrl: "templates/home.html"},
        {url: "/settings", templateUrl: "templates/settings.view.html"},

        {url: "/customers/create", templateUrl: "templates/customer/create.customer.html", controller : "CreateCustomerController"},
        {url: "/customers/edit", templateUrl: "templates/customer/edit.customer.html", controller : "EditCustomerController"},
        {url: "/customers/list", templateUrl: "templates/customer/list.customer.html", controller : "ListCustomerController"},
        {url: "/customers/map", templateUrl: "templates/customer/tracking.customer.html", controller : "TrackCustomerController"},
        
        {url: "/vehicles/create", templateUrl: "templates/vehicle/create.vehicle.html", controller : "CreateVehicleController"},
        {url: "/vehicles/edit", templateUrl: "templates/vehicle/edit.vehicle.html", controller : "EditVehicleController"},
        {url: "/vehicles/list", templateUrl: "templates/vehicle/list.vehicle.html", controller : "ListVehicleController"},

        {url: "/deliveries/create", templateUrl: "templates/delivery/create.delivery.html", controller : "CreateDeliveryController"},
        {url: "/deliveries/edit", templateUrl: "templates/delivery/edit.delivery.html", controller : "EditDeliveryController"},
        {url: "/deliveries/edit/:deliveryId", templateUrl: "templates/delivery/edit.delivery.html", controller : "EditDeliveryController"},
        {url: "/deliveries/list", templateUrl: "templates/delivery/list.bis.delivery.html", controller : "V2ListDeliveryController"},
        {url: "/deliveries/suggest", templateUrl: "templates/delivery/suggestion.delivery.html", controller : "SuggestAssignmentController"},
        
        {url: "/drivers/create", templateUrl: "templates/driver/create.driver.html", controller : "CreateDriverController"},
        {url: "/drivers/edit", templateUrl: "templates/driver/edit.driver.html", controller : "EditDriverController"},
        {url: "/drivers/setVehicle", templateUrl: "templates/driver/setVehicle.driver.html", controller : "SetVehicleController"},
        {url: "/drivers/list", templateUrl: "templates/driver/list.driver.html", controller : "ListDriverController"},
        {url: "/drivers/track", templateUrl: "templates/driver/tracking.driver.html", controller : "TrackDriverController"},
        {url: "/drivers/track/:driverId", templateUrl: "templates/driver/tracking.driver.html", controller : "TrackDriverController"}
	];

	$routeProvider.otherwise({redirectTo: '/home'});

	angular.forEach(routes, function (route) {
        if(route.url != "/login"){
            route.resolve = {
                sess: function ($authentication) {
                    return $authentication.getSession()
                }
            };
        }
        $routeProvider.when(route.url, route);
	});

}]);

