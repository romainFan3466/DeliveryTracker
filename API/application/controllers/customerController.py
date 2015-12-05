from flask import  Blueprint, request, jsonify, abort
from application import db
from application.classes.Location import Location


customer_blueprint = Blueprint('customer', __name__,)



@customer_blueprint.route("/customers", methods=['POST'])
def create():
    customer_data = request.get_json(force=True)
    if (
        "customer" in customer_data and
        "name" in customer_data["customer"] and
        "location" in customer_data["customer"] and
        "lat" in customer_data["customer"]["location"] and
        "lng" in customer_data["customer"]["location"] and
        "phone" in customer_data["customer"]
        ):

        ### check customer name duplication
        if db.is_existing(table="customers", conditions={"name":customer_data["customer"]["name"]}):
            return jsonify(info="Customer with the same name already exist"),400

        # record Location
        locationId = Location.getIdFromDB(dbInstance=db,
                             lat=customer_data["customer"]["location"]["lat"],
                             lng=customer_data["customer"]["location"]["lng"])

        # record customer
        data = {
            "name" : customer_data["customer"]["name"],
            "location_id" : locationId,
            "phone" : customer_data["customer"]["phone"]
        }
        customerId= db.insert(table="customers", params=data)

        return jsonify(info="Customer created successfully", customerId=customerId),200
    else:
        abort(400)



@customer_blueprint.route("/customers/<id>", methods=['PUT'])
def update(id:int):

    ### check existing customer
    if not db.is_existing(table="customers", conditions={"id":id}):
        return jsonify(info="Customer not found"),404

    customer_data = request.get_json(force=True)

    if ("customer" in customer_data):
        customer = {}
        #name
        if "name" in customer_data["customer"]:
            if db.is_existing(table="customers", conditions={"name":customer_data["customer"]["name"]}):
                return jsonify(info="Customer with the same name already exists"),400

            customer["name"] = customer_data["customer"]["name"]

        #location
        if ("location" in customer_data["customer"] and
            "lat" in customer_data["customer"]["location"] and
            "lng" in customer_data["customer"]["location"]
            ):
            customer["location_id"] = Location.getIdFromDB(dbInstance=db,
                                        lat=customer_data["customer"]["location"]["lat"],
                                        lng=customer_data["customer"]["location"]["lng"])
        #phone
        if "phone" in customer_data["customer"]:
            customer["phone"] = customer_data["customer"]

        db.update(table="customers", params=customer, conditions={"id":id})
        return jsonify(info="Customer data updated successfully"),200
    else:
        abort(400)



@customer_blueprint.route("/customers/<id>", methods=['DELETE'])
def delete(id:int):

    existing_customer = db.is_existing(table="customers",conditions={"id": id})
    if existing_customer is False:
        return jsonify(info="Customer not found"),404

    db.delete(table="customers", conditions={"id":id})
    return jsonify(info="Customer deleted successfully"),200



@customer_blueprint.route("/customers/<id>", methods=['GET'])
def get(id:int):
    _SQL = """SELECT customers.*,
            locations.lat AS location_lat ,
            locations.lng AS location_lng
            FROM customers
            INNER JOIN locations ON customers.location_id = locations.id
            WHERE customers.id = %(id)s;
          """

    customer_raw = db.query(_SQL, {"id": id}, multiple=False)
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



@customer_blueprint.route("/customers/all", methods=['GET'])
def getAll():
    _SQL = """SELECT customers.*,
            locations.lat AS location_lat ,
            locations.lng AS location_lng
            FROM customers
            INNER JOIN locations ON customers.location_id = locations.id;
          """
    customers_raw = db.query(_SQL)
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



