from flask import render_template, Blueprint, url_for, redirect, flash, request


authentication_blueprint = Blueprint('authentication', __name__,)


@authentication_blueprint.route("/signIn", methods=['POST'])
def sign_in():
    pass


@authentication_blueprint.route("/logOut", methods=['GET'])
def log_out():
    pass





