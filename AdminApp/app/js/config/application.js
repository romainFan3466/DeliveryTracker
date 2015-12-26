
var AppModule = angular.module('DeliveryTrackerAdmin.app', [
    'ngRoute' ,
    'ngResource',
    'angular.filter']);

AppModule.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    //$httpProvider.defaults.useXDomain = true;
}]);