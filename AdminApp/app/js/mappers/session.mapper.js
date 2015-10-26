/**
 * @ngdoc object
 * @name appModule.object:SessionMapper
 *
 * @description
 * This object parses session data into a SessionMapper object
 *
 *
 */
AppModule.factory('SessionMapper',
    function () {


        var SessionMapper = function (data) {

            /**
             * @ngdoc property
             * @name authenticated
             * @propertyOf appModule.object:SessionMapper
             * @description
             * True if user is authenticated, else false
             * @returns {boolean} identifier
             */
            this.authenticated = false;

            /**
             * @ngdoc property
             * @name uid
             * @propertyOf appModule.object:SessionMapper
             * @description
             * SessionMapper user identifier
             * @returns {string} identifier
             */
            this.uid = "";

            /**
             * @ngdoc property
             * @name email
             * @propertyOf appModule.object:SessionMapper
             * @description
             * SessionMapper user email
             * @returns {string} email
             */
            this.email = "";

            if (angular.isDefined(data)) {
                this.parse(data);
            }
        };

        
        /** @ngdoc method
         * @name parse
         * @methodOf appModule.object:SessionMapper
         * @param {Object} data This object is supposed to have the same propriety than SessionMapper.
         * @description
         * Set all propriety matching by a provided object
         */
        SessionMapper.prototype.parse = function(data){
            if (data) {
                var self = this;
                angular.forEach(data, function (value, key) {
                    self[key] = value;
                });
            }
        };


        return SessionMapper;
    }
);