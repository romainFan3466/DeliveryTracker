
AppModule.factory('SessionMapper',
    function () {


        var SessionMapper = function (data, authenticated) {


            this.authenticated = authenticated;
            this.id = "";
            this.email = "";
            this.companyId = "";
            this.type = "";
            if (angular.isDefined(data)) {
                this.parse(data);
            }
        };

        SessionMapper.prototype.parse = function(data){
            if (data) {
                var self = this;
                angular.forEach(data, function (value, key) {
                    if(key == "company_id"){
                        self.companyId = value;
                    }
                    else {
                        self[key] = value;
                    }

                });
            }
        };


        return SessionMapper;
    }
);