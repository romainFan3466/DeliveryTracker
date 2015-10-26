/**
 * @ngdoc controller
 * @name appModule.controller:NewUserModalController
 * @require $scope
 * @require $authentication
 * @require $modalInstance
 *
 * @description
 *
 * Interacts with template : "newUser.modal.html"
 *
 */
AppModule.controller('NewUserModalController',[
    "$scope", "$modalInstance","$authentication", "$log",
 function ($scope, $modalInstance, $authentication, $log) {

    $scope.credentials = {
        email : "",
        password : "",
        confirmedPassword:"",
        company : "",
        address : "",
        city : "",
        country :"",
        phone : ""
    };


     $scope.success=false;
     $scope.error=false;
     $scope.differentPassword = false;
     $scope.loading=false;
     $scope.differentPassword=false;



    $scope.$watchCollection('credentials', function(newValue){
        $scope.differentPassword = newValue.confirmedPassword!="" &&
            newValue.password!=""&&
            !angular.equals(newValue.confirmedPassword, newValue.password);
    });


     $scope.signUp = function (credentials) {
         $scope.loading= true;

             $authentication.signUp(credentials).then(
                 function (results) {
                     $scope.loading=false;
                     $scope.success=true;
                 },
                 function(){
                     $scope.loading=false;
                     $scope.error=true;
                 });
     };


    $scope.ok = function () {
        $modalInstance.close("succes");
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);