AppModule.run(["$rootScope", "$location", "$authentication","$log",
    function ($rootScope, $location, $authentication, $log) {
        $rootScope.$on("$routeChangeError", function (event, next, current, rejection) {
            $location.path("/login");
        });
    }
]);
