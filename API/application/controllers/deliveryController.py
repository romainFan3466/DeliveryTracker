from flask import render_template, Blueprint, url_for, redirect, flash, request

delivery_blueprint = Blueprint('delivery', __name__,)


@delivery_blueprint.route("/deliveries", methods=['POST'])
def create():
    pass


@delivery_blueprint.route("/deliveries/<id>", methods=['PUT'])
def update(id:int):
    pass


@delivery_blueprint.route("/deliveries/<id>", methods=['DELETE'])
def delete(id:int):
    pass


@delivery_blueprint.route("/deliveries/<id>", methods=['GET'])
def get(id:int):
    pass


@delivery_blueprint.route("/deliveries/all", methods=['GET'])
def getAll():
    pass
