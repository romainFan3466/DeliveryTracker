
AppModule.config(['$routeProvider', function ($routeProvider) {
	var routes = [
		{url: "/login", templateUrl: "templates/login.view.html"},
        {url: "/home", templateUrl: "templates/home.template.html"},
        {url: "/settings", templateUrl: "templates/settings.view.html"}
	];

	$routeProvider.otherwise({redirectTo: '/home'});

	angular.forEach(routes, function (route) {

        /*route.resolve = {
            resolve : "$start"
            };*/
        $routeProvider.when(route.url, route);
	});

}]);