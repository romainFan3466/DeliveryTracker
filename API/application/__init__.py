from flask import Flask, jsonify, redirect, send_file, session, render_template
from flask_mail import Mail
from application.core.DBHandler import DBHandler
from flask.ext.cors import CORS
import os
from simplejson import JSONEncoder
from application.classes.Delivery import Delivery
from application.classes.Driver import Driver
app = Flask(__name__)
cors = CORS(app, resources=r'/*', origins="http://127.0.0.1:*", allow_headers="Content-Type", supports_credentials=True)
# cors = CORS(app)

app.config.update(
    DEBUG=True,
    SECRET_KEY="youwillneverguess",
    UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)),"POD"),
    # mail settings
    MAIL_SERVER='ssl0.ovh.net',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,

    # gmail authentication
    MAIL_USERNAME="contact@romainfanara.com",
    MAIL_PASSWORD="password",

    # mail accounts =
    MAIL_DEFAULT_SENDER='contact@romainfanara.com',

    DB_CONFIG={
            "host": "127.0.0.1",
            "user": "root",
            "password": "jf/b6rb",
            "database": "deliveryTracker",
    },

    GOOGLE_MAPS_KEY = "AIzaSyBZjQHj564q5uyAyWNyh7cK6heAMoVZlvM",
)

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, Delivery) or isinstance(obj, Driver):
                return obj.to_dict()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder


### INSTANCES DECLARATION ###
mail = Mail(app)
db = DBHandler(app.config["DB_CONFIG"])


### IMPORT BLUEPRINTS ####
from application.controllers.customerController import customer_blueprint
from application.controllers.authenticationController import authentication_blueprint
from application.controllers.driverController import driver_blueprint
from application.controllers.deliveryController import delivery_blueprint
from application.controllers.vehicleController import vehicle_blueprint
from application.controllers.assignmentController import assignment_blueprint
from application.controllers.mockController import mock_blueprint
### BLUEPRINTS LOADING ###
app.register_blueprint(customer_blueprint)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(vehicle_blueprint)
app.register_blueprint(driver_blueprint)
app.register_blueprint(delivery_blueprint)
app.register_blueprint(assignment_blueprint)
app.register_blueprint(mock_blueprint)



# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify(info="Bad request, some required fields are not recognized"),400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify(info="Unauthorized access" ),401


@app.errorhandler(500)
def bad_request(error):
    return jsonify(info="Internal error"),500
