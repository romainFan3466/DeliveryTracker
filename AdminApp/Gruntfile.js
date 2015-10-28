// Requirements.
//var generator = require("./config/generator");
//var _ = require("lodash");

module.exports = function (grunt) {

	// Paths.
	var buildPath = "./app";
	var configPath = "./config";
    var appPath = "./app";
    var vendorPath = "./vendors";

	// CLI Asked tasks.
	//var tasks = generator.getTasks(grunt);

	//check task is available
	//var needTarget = generator.needTarget(tasks);


	// Load and parse package config.
	//var pkg = grunt.file.readJSON("package.json");
	//var now = new Date();
	//pkg.version = pkg.version + now.getTime();


	// Load and parse the app locale config file.
	//var appConfig = grunt.file.readJSON(configPath + "/appConfig.json");
	//appConfig.pkg = pkg;

    //Retrieve proprieties of given targetName
    //var targetName = grunt.option("target");
    //var target = generator.getTarget(grunt, appConfig.targets, targetName);

    //generator.setTokensReplace(grunt, gruntConfig, appPath)

	// Retrieve grunt config and init grunt.
	var gruntConfig = grunt.file.readJSON(configPath + "/gruntConfig.json");


	grunt.initConfig({
		//target        : target,
		//pkg           : pkg,
		clean         : gruntConfig.clean,
		bower         : gruntConfig.bower,
		copy          : gruntConfig.copy,
		less          : gruntConfig.less,
		concat        : gruntConfig.concat,
		uglify        : gruntConfig.uglify,
		//htmlmin       : gruntConfig.htmlmin,
		//patternReplace: gruntConfig.patternReplace,
		buildPath     : buildPath,
        appPath       : appPath,
        vendorPath    : vendorPath,
		compress      : gruntConfig.compress,
        configPath    : configPath,
        watch         : gruntConfig.watch,
        //ftpsync       : gruntConfig.ftpsync,
        sync          : gruntConfig.sync,
		sass		  : gruntConfig.sass
        //ngdocs        : gruntConfig.ngdocs,
        //karma         : gruntConfig.karma,
        //ftpush        : gruntConfig.ftpush
	});

	// Load dependencies.

	grunt.loadNpmTasks("grunt-bower-task");
	grunt.loadNpmTasks('grunt-contrib-less');
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	//grunt.loadNpmTasks('grunt-contrib-htmlmin');
	grunt.loadNpmTasks("grunt-contrib-copy");
	grunt.loadNpmTasks("grunt-contrib-clean");
	grunt.loadNpmTasks("grunt-contrib-compress");
	//grunt.loadNpmTasks('grunt-pattern-replace');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-sync');
	grunt.loadNpmTasks('grunt-contrib-sass');
    //grunt.loadNpmTasks('grunt-ftpsync');
    //grunt.loadNpmTasks('grunt-ngdocs');
    //grunt.loadNpmTasks('grunt-karma');
    //grunt.loadNpmTasks('grunt-ftpush');



	// Register tasks.
	grunt.registerTask("minify", ["less", "concat", "uglify"]);

// Main Archive Task.

    //Git project task
    grunt.registerTask("deploy-git",  ["sync"]);

    // Main Task.
    grunt.registerTask("deploy", ["clean:post-deploy","minify", "copy","patternReplace","clean:pre-deploy", "ftpush"]);

    // Doc Task.
    grunt.registerTask("doc", ["clean:doc","ngdocs", "ftpush"]);

    // Default task.
    grunt.registerTask("default", ["bower", "deploy"]);


};
