AppModule.config(["$stateProvider", "$urlRouterProvider",
    function ($stateProvider, $urlRouterProvider) {

        var states = [
            {
                state: "app",
                route: {
                    url: '/app',
                    abstract: true,
                    templateUrl: 'templates/menu.html'
                }
            },
            {
                state: "app.deliveries",
                route: {
                    url: '/deliveries',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/deliveries.html',
                            controller: "DeliveriesController"
                        }
                    }
                }
            },
            {
                state: "app.deliveriesAll",
                route: {
                    url: '/deliveries/all',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/all.deliveries.html',
                            controller : "DeliveriesAllController"
                        }
                    }
                }
            },
            {
                state: "app.deliveriesProgress",
                route: {
                    url: '/deliveries/progress',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/progress.deliveries.html',
                            controller : "DeliveriesProgressController"
                        }
                    }
                }
            },
            {
                state: "app.deliveriesIncoming",
                route: {
                    url: '/deliveries/incoming',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/incoming.deliveries.html',
                            controller : "DeliveriesIncomingController"
                        }
                    }
                }
            },
            {
                state: "app.single",
                route: {
                    url: '/deliveries/id/:deliveryId',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/delivery.html',
                            controller : "DeliveryController"
                        }
                    }
                }
            },
            {
                state: "app.login",
                route: {
                    url: '/login',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/login.html',
                            controller : "LoginController"
                        }
                    }
                }
            },
             {
                state: "app.debug",
                route: {
                    url: '/debug',
                    views: {
                        'menuContent': {
                            templateUrl: 'templates/debug.html',
                            controller : "DebugController"
                        }
                    }
                }
            }


        ];

        angular.forEach(states, function (state) {
            if (state.state != "app.login" && state.state != "app.debug" && state.state != "app") {
                state.route.resolve = {
                    sess: function ($authentication) {
                        return $authentication.getSession();
                    }
                };
            }
            $stateProvider.state(state.state, state.route);
        });


        // if none of the above states are matched, use this as the fallback
        $urlRouterProvider.otherwise('/app/deliveries');
    }
]);