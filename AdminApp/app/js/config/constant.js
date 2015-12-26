/**
 * @ngdoc object
 * @name appModule.object:Config
 *
 * @description
 * Config is a global object regrouping constant variables for the entire app.
 *
 *
 */
AppModule.constant('Config', {
    /**
     * @ngdoc property
     * @name baseUrl
     * @propertyOf appModule.object:Config
     * @description
     * Base Url of the API.
     *
     * The rest of the URL is completed by services, depends of the methods.
     * @returns {String} baseUrl
     */
    baseUrl : "http://127.0.0.1:5000/api"
});
