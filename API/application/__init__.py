from flask import Flask, jsonify
from flask_mail import Mail
from application.core.DBHandler import DBHandler
app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SECRET_KEY="youwillneverguess",

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

    # DB config
    DB_HOST="127.0.0.1",
    DB_USER="root",
    DB_PASSWORD="jf/b6rb",
    DB_DATABASE="deliveryTracker",

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
db = DBHandler(app.config["DB_CONFIG"])


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





