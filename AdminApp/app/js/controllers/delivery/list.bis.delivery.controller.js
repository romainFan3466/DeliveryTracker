AppModule.controller("V2ListDeliveryController", [
    "$scope", "$log", "$uibModal", "$location","$delivery","$filter",
    function ($scope, $log, $uibModal, $location, $delivery, $filter) {


        $scope.vm = {};
        $scope.view = {
            calendarView : 'month',
            viewDate :  new Date()
        };
        //$scope.vm.events = [
        //    {
        //        title: 'An event',
        //        type: 'warning',
        //        startsAt: moment().startOf('week').subtract(2, 'days').add(8, 'hours').toDate(),
        //        draggable: true,
        //        resizable: true
        //    },
        //    {
        //        title: 'An event',
        //        type: 'warning',
        //        startsAt: moment().startOf('week').subtract(2, 'days').add(8, 'hours').toDate(),
        //        draggable: true,
        //        resizable: true
        //    }, {
        //        title: '<i class="glyphicon glyphicon-asterisk"></i> <span class="text-primary">Another event</span>, with a <i>html</i> title',
        //        type: 'info',
        //        startsAt: moment().subtract(1, 'day').toDate(),
        //        endsAt: moment().add(5, 'days').toDate(),
        //        draggable: true,
        //        resizable: true
        //    }, {
        //        title: 'This is a really long event title that occurs on every year',
        //        type: 'important',
        //        startsAt: moment().startOf('day').add(7, 'hours').toDate(),
        //        endsAt: moment().startOf('day').add(19, 'hours').toDate(),
        //        recursOn: 'year',
        //        draggable: true,
        //        resizable: true
        //    }];



        $scope.$watchCollection("view", function(view){
            var dateView, start, end;
            switch(view.calendarView){
                case "month":
                    dateView = $scope.view.viewDate;
                    start = new Date(dateView.getFullYear(), dateView.getMonth(),1);
                    end = new Date(dateView.getFullYear(), dateView.getMonth()+1,0);
                    getDeliveries(start, end);
                    break;
                case "year":
                    dateView = $scope.view.viewDate;
                    start = new Date(dateView.getFullYear(), 1,1);
                    end = new Date(dateView.getFullYear()+1, 0,0);
                    getDeliveries(start, end);
                    break;
                default :
                    $scope.deliveries = [];

            }
        });

        var getDelivery = function(id){
            var d = null;
            angular.forEach($scope.deliveries, function(delivery){
               if(delivery.id == id){
                   d= delivery;
               }
            });
            return d;
        };

        var getDeliveries = function(start, end){
            var s = $filter('date')(start, "yyyy-MM-dd HH:mm:ss");
            var e = $filter('date')(end, "yyyy-MM-dd HH:mm:ss");
            $delivery.getAll({start : s, end:e}).then(
                function(res){
                    $scope.deliveries = res.deliveries;
                    $scope.vm.events = [];
                    angular.forEach($scope.deliveries, function(delivery){
                        var event = {
                            title: delivery.customerName +" : "+ delivery.content ,
                            type: 'info',
                            startsAt:new Date(delivery.dateDue),
                            id : delivery.id
                        };
                        $scope.vm.events.push(event);
                    });
                },
                function(res){
                    $log.log("load deliveries failed");
                }
            )
        };


        $scope.vm.isCellOpen = true;
        $scope.vm.eventClicked = function (event) {
            var delivery = getDelivery(event.id);
            var modalInstance = $uibModal.open({
                animation: true,
                size : "lg",
                templateUrl: 'templates/delivery/deliveryModal.html',
                controller: 'DeliveryModalController',
                resolve: {
                    selectedDelivery: function () {
                        return delivery;
                    }
                }
            });

            modalInstance.result.then(function () {

            }, function () {

            });
        };

        $scope.vm.toggle = function ($event, field, event) {
            $event.preventDefault();
            $event.stopPropagation();
            event[field] = !event[field];
        };

        $scope.vm.viewChangeClicked = function (nextView) {
            if (nextView === 'day' || nextView === 'week') {
                return false;
            }
        };


    }
]);
