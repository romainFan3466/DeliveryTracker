/**
 * @ngdoc controller
 * @name appModule.controller:LoginController
 * @require $scope
 * @require $authentication
 * @require $location
 * @require $modal
 *
 * @description
 *
 * Interacts with template : "login.view.html"
 *
 */
AppModule.controller("LoginController",[
    "$scope", "$log", "$modal", "$authentication", "$location",
    function ($scope, $log, $modal, $authentication, $location) {

        $scope.login = {
            email : "",
            password : ""
        };


        $scope.signupCredentials = {
            email:'',
            password:'',
            confirmedPassword:""
        };

        $scope.loading=false;
        $scope.wrongCredentials=false;


        $scope.loginIn = function (credentials) {
            $scope.loading=true;
            $authentication.loginIn(credentials).then(
                function (result) {
                    $scope.loading=false;
                    $location.path("/home");
                },
                function(result){
                    $scope.loading=false;
                    $scope.wrongCredentials=true;
                }

            );
        };





        $scope.logout = function () {
            $authentication.logout().then(function (results) {
            });
        };


    $scope.openNewUserModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'html/views/newUser.modal.html',
            controller: 'NewUserModalController'
        });

        modalInstance.result.then(
            //result from login modal
            function (info) {

        },
            //fail from login modal
            function () {
            $log.info('Error create user request : ' + new Date());
        });
    };


}]);

