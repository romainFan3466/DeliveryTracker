from flask import  Blueprint, request, jsonify, abort, session
from application import db
from application.classes.Location import Location
import application.decorators.sessionDecorator as sessionDecorator


customer_blueprint = Blueprint('customer', __name__,)


@customer_blueprint.route("/api/customers", methods=['POST'])
@sessionDecorator.required_user("admin")
def create():
    customer_data = request.get_json(force=True)
    if (
        "customer" in customer_data and
        "name" in customer_data["customer"] and
        "location" in customer_data["customer"] and
        "lat" in customer_data["customer"]["location"] and
        "lng" in customer_data["customer"]["location"] and
        "phone" in customer_data["customer"] and
        Location.isValid(**customer_data["customer"]["location"])
        ):

        ### check customer name duplication
        company_id = session["user"]["company_id"]
        if db.is_existing(table="customers",
                          conditions={"name":customer_data["customer"]["name"], "company_id":company_id}):
            return jsonify(info="Customer with the same name already exist"),400


        # record customer
        data = {
            "name" : customer_data["customer"]["name"],
            "location_lat" : customer_data["customer"]["location"]["lat"],
            "location_lng" : customer_data["customer"]["location"]["lng"],
            "phone" : customer_data["customer"]["phone"],
            "company_id" : company_id
        }
        customerId= db.insert(table="customers", params=data)

        return jsonify(info="Customer created successfully", customerId=customerId),200
    else:
        abort(400)



@customer_blueprint.route("/api/customers/<id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def update(id:int):
    company_id = session["user"]["company_id"]
    ### check existing customer
    if not db.is_existing(table="customers", conditions={"id":id, "company_id": company_id}):
        return jsonify(info="Customer not found"),404

    customer_data = request.get_json(force=True)

    if ("customer" in customer_data):
        customer = {}
        #name
        if "name" in customer_data["customer"]:
            if db.is_existing(table="customers", conditions={"name":customer_data["customer"]["name"],"company_id": company_id}):
                return jsonify(info="Customer with the same name already exists"),400

            customer["name"] = customer_data["customer"]["name"]

        #location
        if ("location" in customer_data["customer"] and
            "lat" in customer_data["customer"]["location"] and
            "lng" in customer_data["customer"]["location"] and
            Location.isValid(**customer_data["customer"]["location"])
            ):
            customer["location_lat"] = customer_data["customer"]["location"]["lat"]
            customer["location_lng"] = customer_data["customer"]["location"]["lng"]

        #phone
        if "phone" in customer_data["customer"]:
            customer["phone"] = customer_data["customer"]["phone"]

        db.update(table="customers", params=customer, conditions={"id":id})
        return jsonify(info="Customer data updated successfully"),200
    else:
        abort(400)



@customer_blueprint.route("/api/customers/<id>", methods=['DELETE'])
@sessionDecorator.required_user("admin")
def delete(id:int):
    company_id = session["user"]["company_id"]
    existing_customer = db.is_existing(table="customers",conditions={"id": id, "company_id": company_id})
    if existing_customer is False:
        return jsonify(info="Customer not found"),404

    db.delete(table="customers", conditions={"id":id})
    return jsonify(info="Customer deleted successfully"),200



@customer_blueprint.route("/api/customers/<id>", methods=['GET'])
@sessionDecorator.required_user("admin")
def get(id:int):
    company_id = session["user"]["company_id"]
    customer_raw = db.select(table="customers", conditions={"id": id, "company_id": company_id}, multiple=False)
    if customer_raw is None:
        return jsonify(info="Customer not found"),404

    customer = {
        "id": customer_raw["id"],
        "name" : customer_raw["name"],
        "phone" : customer_raw["phone"],
        "location": {
            "lat": customer_raw["location_lat"],
            "lng": customer_raw["location_lng"],
        }
    }
    return jsonify(customer=customer),200


@customer_blueprint.route("/api/customers/all", methods=['GET'])
@sessionDecorator.required_user("admin")
def getAll():
    company_id = session["user"]["company_id"]
    customers_raw = db.select(table="customers",conditions={"company_id": company_id})
    if len(customers_raw) <1:
        return jsonify(customers=customers_raw), 200

    customers = []
    for customer in customers_raw:
        c = {
            "customer": {
                "id": customer["id"],
                "name": customer["name"],
                "phone": customer["phone"],
                "location": {
                    "lat": customer["location_lat"],
                    "lng": customer["location_lng"],
                }
            }
        }
        customers.append(c)

    return jsonify(customers=customers),200
