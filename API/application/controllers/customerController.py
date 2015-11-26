from flask import  Blueprint, url_for, redirect, request, jsonify, abort
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

        ### check customer name duplication
        if db.is_existing(table="customers", conditions={"name":customer_data["customer"]["name"]}):
            return jsonify(info="Customer with the same name already exist"),400

        # record Location
        # TODO: check existing location
        locationId = db.insert(table="locations", params=customer_data["customer"]["location"])

        # record customer
        data = {
            "name" : customer_data["customer"]["name"],
            "locationId" : locationId,
            "phone" : customer_data["customer"]["phone"],
        }
        customerId= db.insert(table="customers", params=data)

        return jsonify(info="Customer created successfully", customerId=customerId),200
    else:
        abort(400)



## TODO : need to test
@customer_blueprint.route("/customers/<id>", methods=['PUT'])
def update(id:int):

    ### check existing customer
    if not db.is_existing(table="customers", conditions={"id":id}):
        return jsonify(info="Customer id not found"),404

    customer_data = request.get_json(force=True)

    if ("customer" in customer_data):

        ### check customer name duplication
        if ("name" in customer_data["customer"] and
            db.is_existing(table="customers", conditions={"name":customer_data["customer"]["name"]})
            ):
            return jsonify(info="Customer with the same name already exist"),400

        ### update customer
        db.update(table="customers", params=customer_data["customer"], conditions={"id":id})
        return jsonify(info="Customer data updated successfully"),200
    else:
        abort(400)



@customer_blueprint.route("/customers/<id>", methods=['DELETE'])
def delete(id:int):

    existing_customer = db.is_existing(table="customers",conditions={"id": id})
    if existing_customer is False:
        return jsonify(info="Customer not found"),404

    deleted = db.delete(table="customers", conditions={"id":id})
    if deleted:
        return jsonify(info="Customer deleted successfully"),200
    return abort(500)



@customer_blueprint.route("/customers/<id>", methods=['GET'])
def get(id:int):
    customer = db.select(table="customers",selected_columns=("*",), conditions={"id":id}, multiple=False)
    if customer is None:
        return jsonify(info="Customer not found"),404
    return jsonify(customer=customer),200



@customer_blueprint.route("/customers/all", methods=['GET'])
def getAll():
    return jsonify(customers=db.select(table="customers", selected_columns=('*',))),200



