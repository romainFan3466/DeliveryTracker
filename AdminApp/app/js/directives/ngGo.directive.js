/**
 * @ngdoc directive
 * @name appModule.directive:ngGo
 * @element ANY
 * @restrict A

 @param {expression} ngGo  Path expression to evaluate and go to it

 * @description
 * When you click on the current element, you will be redirected to the provided path
 */
AppModule.directive("ngGo", function ($location) {
    return {
        restrict  : "A",
        scope     : {
        },
        link : function (scope, element, attrs) {

            element.on('mouseover',function(){
                element.css("cursor","pointer");
            });

            element.on('click',function(){
                scope.$apply($location.path(attrs.ngGo));
            });
        }
    }
});
