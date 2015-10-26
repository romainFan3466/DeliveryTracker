/**
 * @ngdoc directive
 * @name appModule.directive:spinner
 * @element ANY
 * @restrict E
 * @param {expression} loading  Allow to show/hide the directive
 *
 * @description
 * This directive allows to display a loading spinner.
 *
 * You must provide an expression to evaluate by the attribute **loading**
 *
 *
 */
AppModule.directive("spinner", function () {
    return {
        restrict  : "E",
        scope     : {
            loading: "="
        },
        replace : true,
        template : '<div class="spinner-global  ng-cloak" ng-cloak ng-show="loading">' +
        '<div class ="spinner-img fa fa-refresh fa-spin fa-5x"></div>' +
        '</div>'
    }
});
