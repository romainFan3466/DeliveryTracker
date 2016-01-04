
var AppModule = angular.module('DeliveryTrackerAdmin.app', [
    'ngRoute' ,
    'ngResource',
    'angular.filter',
    'ui.bootstrap',
    'uiGmapgoogle-maps']);

AppModule.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    //$httpProvider.defaults.useXDomain = true;
}]);