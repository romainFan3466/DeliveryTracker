from flask import render_template, Blueprint, url_for, redirect, flash, request


driver_blueprint = Blueprint('driver', __name__,)


@driver_blueprint.route("/drivers", methods=['POST'])
def create():
    pass


@driver_blueprint.route("/drivers/<id>", methods=['PUT'])
def update(id:int):
    pass


@driver_blueprint.route("/drivers/<id>", methods=['DELETE'])
def delete(id:int):
    pass


@driver_blueprint.route("/drivers/<id>", methods=['GET'])
def get(id:int):
    pass


@driver_blueprint.route("/drivers/all", methods=['GET'])
def getAll():
    pass


@driver_blueprint.route("/drivers/<vehicleID>/deliveries/<deliveryID>", methods=['PUT'])
def assign_Delivery(vehicleID:int, deliveryID:int):
    pass