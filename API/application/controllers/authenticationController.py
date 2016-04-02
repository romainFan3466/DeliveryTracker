from flask import abort, Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from application import db
from application.classes.User import User

authentication_blueprint = Blueprint('authentication', __name__,)


@authentication_blueprint.route("/api/signIn", methods=['POST'])
def sign_in():
    user_req = request.get_json(force=True)
    user = User.parse(user_req, "create")
    if "errors" in user :
        return jsonify(errors=user["errors"]), 400

        #check user exist
    cond = {
        "email" : user_req["user"]["email"],
        "type" : user_req["user"]["type"]
    }
    user = db.select(table="users", conditions=cond, multiple=False)

    if user is None :
        return jsonify(info="Bad Credentials"),400

    if check_password_hash(user["password"],user_req["user"]["password"]):

        session["user"] = {
                    "id" : user["id"],
                    "email":  user["email"],
                    "name" : user["name"],
                    "type": user["type"],
                    "company_id": user["company_id"],
        }
        session.permanent = True
        return jsonify(session=session["user"], info="Your are currently logged in"), 200
    else:
        return jsonify(info="Bad Credentials"),400


@authentication_blueprint.route("/api/logOut", methods=['GET', "OPTIONS"])
def log_out():
    if "user" in session:
        session.pop("user")
    return jsonify(info="Your are logged out"), 200


@authentication_blueprint.route("/api/status", methods=['GET'])
def status():
    va = request
    if "user" in session :
        return jsonify(session=session["user"])
    return jsonify(session="logout")
