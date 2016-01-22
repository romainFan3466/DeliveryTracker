
var AppModule = angular.module('DeliveryTrackerAdmin.app', [
    'ngRoute' ,
    'ngResource',
    'ngSanitize',
    'angular.filter',
    'ui.bootstrap',
    'mwl.calendar',
    'uiGmapgoogle-maps']);

AppModule.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    //$httpProvider.defaults.useXDomain = true;
}]);