AppModule.run(["$rootScope", "$ionicPlatform", "$state", "$log", "$cordovaDialogs", "$ionicHistory", "$interval",
    function ($rootScope, $ionicPlatform, $state, $log, $cordovaDialogs, $ionicHistory, $interval) {
        $rootScope.positionInterval = null;
        $rootScope.uploadCount = 0;

        function onRequestSuccess(success) {
        }

        function onRequestFailure(error) {
            console.error("Accuracy request failed: error code= " + error);
            if (error.code !== cordova.plugins.locationAccuracy.ERROR_USER_DISAGREED) {
                if (window.confirm("Failed to automatically set Location Mode to 'High Accuracy'. Would you like to switch to the Location Settings page and do this manually?")) {
                    cordova.plugins.diagnostic.switchToLocationSettings();
                }
            }
            else {
                navigator.app.exitApp();
            }
        }

        $rootScope.$on('$stateChangeError',
            function (event, toState, toParams, fromState, fromParams, error) {
                $state.go("app.login");
            });


        $rootScope.$on('$stateChangeSuccess',
            function (event, toState, toParams, fromState, fromParams, error) {
                if (toState.name && toState.name != "app.login" && toState.name != "app.debug" && toState.name != "app") {
                    if ($rootScope.positionInterval == null) {
                        $rootScope.positionInterval = $interval(function () {
                            $rootScope.uploadCount++;
                            $rootScope.$broadcast('upload-counter');
                            $log.log("update positon...");
                        }, 5000);
                    }
                }
            });


        $ionicPlatform.ready(function () {
            // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
            // for form inputs)
            if (window.cordova && window.cordova.plugins.Keyboard) {
                cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
                cordova.plugins.Keyboard.disableScroll(true);

            }
            if (window.StatusBar) {
                // org.apache.cordova.statusbar required
                StatusBar.styleDefault();
            }


            $ionicPlatform.registerBackButtonAction(function () {
                if ($ionicHistory.backView() != null) {
                    $ionicHistory.goBack();
                }
                else {
                    $cordovaDialogs.confirm('Leave ?', '', ['No', 'Yes'])
                        .then(function (buttonIndex) {
                            // no button = 0, 'OK' = 1, 'Cancel' = 2
                            if (buttonIndex == 2) {
                                navigator.app.exitApp();
                            }
                        }
                    );
                }
            }, 100);


            if (cordova) {
                cordova.plugins.locationAccuracy.request(onRequestSuccess, onRequestFailure, cordova.plugins.locationAccuracy.REQUEST_PRIORITY_HIGH_ACCURACY);

                cordova.plugins.backgroundMode.setDefaults({
                            title: 'LocationProcess',
                            text: 'Executing background locations.'
                        });

                cordova.plugins.backgroundMode.enable();

                cordova.plugins.backgroundMode.onactivate = function () {
                    setTimeout(function () {
                        cordova.plugins.backgroundMode.configure({
                            text: 'Live tracking running'
                        });
                    }, 2000);
                };

                cordova.plugins.backgroundMode.ondeactivate = function () {};
            }
        });
    }
]);