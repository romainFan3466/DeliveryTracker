from flask import  Blueprint, request, jsonify, abort, session
from application import db
from application.classes.Location import Location
import application.decorators.sessionDecorator as sessionDecorator
from application.classes.Customer import Customer


customer_blueprint = Blueprint('customer', __name__,)


@customer_blueprint.route("/api/customers", methods=['POST'])
@sessionDecorator.required_user("admin")
def create():
    req = request.get_json(force=True)
    customer = Customer.parse(req, "create")
    if "errors" in customer:
        return jsonify(errors=customer["errors"]),400
    customer = customer["customer"]

    ### check customer name duplication
    company_id = session["user"]["company_id"]
    if db.is_existing(table="customers",
                      conditions={"name":customer["name"], "company_id":company_id}):
        return jsonify(info="Customer with the same name already exist"),400

    # record customer
    data = {
        "name" : customer["name"],
        "address" : customer["address"],
        "location_lat" : customer["location"]["lat"],
        "location_lng" : customer["location"]["lng"],
        "phone" : customer["phone"],
        "company_id" : company_id
    }
    customerId= db.insert(table="customers", params=data)
    return jsonify(info="Customer created successfully", customerId=customerId),200


@customer_blueprint.route("/api/customers/<id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def update(id:int):
    company_id = session["user"]["company_id"]
    ### check existing customer
    if not db.is_existing(table="customers", conditions={"id":id, "company_id": company_id}):
        return jsonify(info="Customer not found"),404

    req = request.get_json(force=True)
    req = Customer.parse(req, "update")

    if "errors" in req:
        return jsonify(errors=req["errors"]),400
    req = req["customer"]
        
    customer = {}
    #name
    if "name" in req:
        if db.is_existing(table="customers", conditions={"name":req["name"],"company_id": company_id}):
            return jsonify(info="Customer with the same name already exists"),400

        customer["name"] = req["name"]

    #address
    if "address" in req:
        customer["address"] = req["address"]

    #location
    if "location" in req :
        customer["location_lat"] = req["location"]["lat"]
        customer["location_lng"] = req["location"]["lng"]

    #phone
    if "phone" in req:
        customer["phone"] = req["phone"]

    db.update(table="customers", params=customer, conditions={"id":id})
    return jsonify(info="Customer data updated successfully"),200



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
@sessionDecorator.required_user()
def get(id:int):
    company_id = session["user"]["company_id"]
    customer_raw = db.select(table="customers", conditions={"id": id, "company_id": company_id}, multiple=False)
    if customer_raw is None:
        return jsonify(info="Customer not found"),404

    customer = {
        "id": customer_raw["id"],
        "name" : customer_raw["name"],
        "phone" : customer_raw["phone"],
        "address" : customer_raw["address"],
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
                "address" : customer["address"],
                "location": {
                    "lat": customer["location_lat"],
                    "lng": customer["location_lng"],
                }
            }
        }
        customers.append(c)

    return jsonify(customers=customers),200
