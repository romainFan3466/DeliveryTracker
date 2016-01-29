// Requirements.
//var generator = require("./config/generator");
//var _ = require("lodash");

module.exports = function (grunt) {

	// Paths.
	//var buildPath = "../API/application/templates";
	var buildPath = "./www";
	var configPath = ".";
    var appPath = "./www";
    var vendorPath = "./www/lib";

	var gruntConfig = grunt.file.readJSON(configPath + "/gruntConfig.json");


	grunt.initConfig({
		clean         : gruntConfig.clean,
		less          : gruntConfig.less,
		concat        : gruntConfig.concat,
		uglify        : gruntConfig.uglify,
		buildPath     : buildPath,
        appPath       : appPath,
        vendorPath    : vendorPath,
        configPath    : configPath,
        watch         : gruntConfig.watch,
		sass		  : gruntConfig.sass
	});

	// Load dependencies.

	grunt.loadNpmTasks('grunt-contrib-less');
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks("grunt-contrib-clean");
    grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-sass');



	// Register tasks.
	grunt.registerTask("minify", ["less", "concat"]);

// Main Archive Task.

    //Git project task
    grunt.registerTask("deploy-git",  ["sync"]);

    // Main Task.
    grunt.registerTask("deploy", ["clean:pre-deploy","minify"]);


    // Default task.
    grunt.registerTask("default", ["bower", "deploy"]);


};
