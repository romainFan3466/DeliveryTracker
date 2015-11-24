from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify, abort
from application import db


customer_blueprint = Blueprint('customer', __name__,)

@customer_blueprint.route("/customers", methods=['POST'])
def create():
    customer_data = request.get_json(force=True)
    if (
        "customer" in customer_data and
        "name" in customer_data["customer"] and
        "location" in customer_data["customer"] and
        "phone" in customer_data["customer"]
        ):

        # record Location
        # TODO: check existing location
        locationId = db.insert("locations", params=customer_data["customer"]["location"])

        # record customer
        data = {
            "name" : customer_data["customer"]["name"],
            "locationId" : locationId,
            "phone" : customer_data["customer"]["phone"],
        }
        customerId= db.insert("customers", params=data)

        return jsonify(info="Customer created successfully", customerId=customerId),200
    else:
        abort(400)



@customer_blueprint.route("/customers/<id>", methods=['PUT'])
def update(id:int):

    if db.is_existing(table="customers", conditions={id:id}):
        return jsonify(info="Customer id not found"),404

    customer_data = request.get_json(force=True)

    if ("customer" in customer_data):
        db.update("customers", params=customer_data["customer"])
        return jsonify(info="Customer data updated successfully"),200
    else:
        abort(400)


@customer_blueprint.route("/customers/<id>", methods=['DELETE'])
def delete(id:int):
    pass


@customer_blueprint.route("/customers/<id>", methods=['GET'])
def get(id:int):
    pass


@customer_blueprint.route("/customers/all", methods=['GET'])
def getAll():
    pass


