from flask import render_template, Blueprint, url_for, redirect, flash, request

from application import app

vehicle_blueprint = Blueprint('vehicle', __name__,)


@vehicle_blueprint.route("/vehicles", methods=['POST'])
def create():
    pass


@vehicle_blueprint.route("/vehicles/<id>", methods=['PUT'])
def update(id:int):
    pass


@vehicle_blueprint.route("/vehicles/<id>", methods=['DELETE'])
def delete(id:int):
    pass


@vehicle_blueprint.route("/vehicles/<id>", methods=['GET'])
def get(id:int):
    pass


@vehicle_blueprint.route("/vehicles/all", methods=['GET'])
def getAll():
    pass
