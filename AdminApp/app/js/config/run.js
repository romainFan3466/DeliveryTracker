AppModule.run(["$rootScope", "$location", "$authentication","$log",
    function ($rootScope, $location, $authentication, $log) {
        $rootScope.$on("$routeChangeError", function (event, next, current, rejection) {
            //$authentication.getSession().then(
            //    function(result){
            //        var auth = $authentication.isAuthenticated();
            //        if(auth ==false){
            //            event.preventDefault();
            //            $location.path("/login");
            //        }
            //    },
            //
            //    function(result){
            //        event.preventDefault();
            //        $location.path("/login");
            //    }
            //);
            //var auth = $authentication.isAuthenticated();
            //if (auth == false) {
            //    event.preventDefault();
            //    $location.path("/login");
            //}

            $location.path("/login");

        });
    }
]);
