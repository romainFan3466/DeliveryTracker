
var AppModule = angular.module('DeliveryTrackerMobile.app', [
    'ionic',
    'ngCordova'
]);

AppModule.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    //$httpProvider.defaults.useXDomain = true;
}]);

//AppModule.config(function($compileProvider ){
//  $compileProvider.aHrefSanitizationWhitelist(/^\s*(geo):/);
//});
