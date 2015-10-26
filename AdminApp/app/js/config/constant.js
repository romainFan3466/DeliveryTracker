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
    baseUrl : "http://",
    TVA : 0.20
});
