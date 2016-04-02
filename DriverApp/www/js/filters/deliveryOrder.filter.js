AppModule.filter('deliveryOrder', [
        "$filter",
        function ($filter) {
            return function (deliveries, reverse) {

                deliveries = deliveries || [];
                reverse  = angular.isDefined(reverse)? reverse : false;
                var out = [];

                //deliveries
                var _notTaken = $filter('filter')(deliveries, {state: "not taken"}, true);
                var _taken = $filter('filter')(deliveries, {state: "taken"}, true);
                var _pickedUp = $filter('filter')(deliveries, {state: "picked up"}, true);
                var _onWay = $filter('filter')(deliveries, {state: "on way"}, true);
                var _delivered = $filter('filter')(deliveries, {state: "delivered"}, true);
                var _canceled = $filter('filter')(deliveries, {canceled: true}, true);

                //sort by numOrder


                _notTaken = $filter('orderBy')(_notTaken, "numOrder", reverse);
                _taken = $filter('orderBy')(_taken, "numOrder", reverse);
                _pickedUp = $filter('orderBy')(_pickedUp, "numOrder", reverse);
                _onWay = $filter('orderBy')(_onWay, "numOrder", reverse);
                _delivered = $filter('orderBy')(_delivered, "numOrder", reverse);
                _canceled = $filter('orderBy')(_canceled, "numOrder", reverse);
                //if(reverse == true){
                //    out = out.concat(_canceled,_delivered, _onWay, _pickedUp ,_taken, _notTaken);
                //}
                //else {
                //    out = out.concat(_notTaken, _taken, _pickedUp, _onWay, _delivered, _canceled);
                //}

                out = out.concat(_notTaken, _taken, _pickedUp, _onWay, _delivered, _canceled);


                return out;
            }
        }]
);

