import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, '/home/romain/Documents/DeliveryTrackerProject/API/')

import pytest

from flask import Flask, jsonify
from flask_mail import Mail
from application.core.DBHandler import DBHandler
import os




@pytest.fixture
def app():

    app = Flask(__name__)

    app.config.update(
        DEBUG=True,
        SECRET_KEY="youwillneverguess",

        UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"POD"),

        DB_CONFIG={
                "host": "127.0.0.1",
                "user": "root",
                "password": "jf/b6rb",
                "database": "deliveryTracker",
        },

        GOOGLE_MAPS_KEY = "AIzaSyBZjQHj564q5uyAyWNyh7cK6heAMoVZlvM",
    )


    ### INSTANCES DECLARATION ###
    mail = Mail(app)


    ### IMPORT BLUEPRINTS ####
    from application.controllers.customerController import customer_blueprint
    from application.controllers.authenticationController import authentication_blueprint
    from application.controllers.driverController import driver_blueprint
    from application.controllers.deliveryController import delivery_blueprint
    from application.controllers.vehicleController import vehicle_blueprint


    ### BLUEPRINTS LOADING ###
    app.register_blueprint(customer_blueprint)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(driver_blueprint)
    app.register_blueprint(delivery_blueprint)
    app.register_blueprint(vehicle_blueprint)


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(info="Bad request, some required fields are not recognized"),400


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify(info="Unauthorized access" ),401


    @app.errorhandler(500)
    def bad_request(error):
        return jsonify(info="Internal error"),500



    return app
