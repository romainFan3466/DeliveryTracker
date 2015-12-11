from flask import abort, Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from application import db

authentication_blueprint = Blueprint('authentication', __name__,)


@authentication_blueprint.route("/signIn", methods=['POST'])
def sign_in():
    user_req = request.get_json(force=True)
    if(
       "user" in user_req and
        "email" in user_req["user"] and
        "password" in user_req["user"]
    ):
        #check user exist
        cond = {
            "email" : user_req["user"]["email"],
        }
        user = db.select(table="users", conditions=cond, multiple=False)

        if user is None :
            return jsonify(info="Bad Credentials"),400

        if check_password_hash(user["password"],user_req["user"]["password"]):

            session["user"] = {
                        "id" : user["id"],
                        "email":  user["email"],
                        "type": user["type"],
                        "company_id": user["company_id"],
            }
            return jsonify(info="Your are currently logged in"), 200
        else:
            return jsonify(info="Bad Credentials"),400
    else :
        abort(400)


@authentication_blueprint.route("/logOut", methods=['GET'])
def log_out():
    if "user" in session:
        session.pop("user")
    return jsonify(info="Your are logged out"), 200





