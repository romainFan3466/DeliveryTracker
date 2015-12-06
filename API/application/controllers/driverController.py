from flask import Blueprint, request, abort, jsonify
from application import db
import application.controllers.deliveryController as deliveries

driver_blueprint = Blueprint('driver', __name__,)


@driver_blueprint.route("/drivers", methods=['POST'])
def create():
    driver = request.get_json(force=True)

    if(
        "driver" in driver and
        "name" in driver["driver"] and
        "customer_id" in driver["driver"] and
        "phone" in driver["driver"]
    ):
        if not db.is_existing(table="customers", conditions={"id":driver["driver"]["customer_id"]}):
            return jsonify(info="Customer not found"), 404

        if db.is_existing(table="users",
                          conditions={"name": driver["driver"]["name"], "type":"driver", "customer_id":driver["driver"]["customer_id"]}):
            return jsonify(info="Driver with the same name already exist"),400

        driver_data={
            "name" : driver["driver"]["name"],
            "customer_id" : driver["driver"]["customer_id"],
            "phone" : driver["driver"]["phone"],
            "type":"driver"
        }
        driverId = db.insert(table="users", params=driver_data)
        return jsonify(info="Driver created successfully", driverId=driverId),200
    else :
        abort(400)


#TODO select driver instead is_existing
@driver_blueprint.route("/drivers/<id>", methods=['PUT'])
def update(id:int):
    if not db.is_existing(table="users", conditions={"id":id, "type":"driver"}):
        return jsonify(info="Driver not found"), 404

    driver = request.get_json(force=True)
    if "driver" in driver:
        driver_data = {}

        if "customer_id" in driver["driver"]:
            if not db.is_existing(table="customers", conditions={"id":driver["driver"]["customer_id"]}):
                return jsonify(info="Customer not found"), 404
            driver_data["customer_id"] = driver["driver"]["customer_id"]

        if "name" in driver["driver"]:
            if db.is_existing(table="users",
                          conditions={"name": driver["driver"]["name"], "type":"driver", "customer_id":driver["driver"]["customer_id"]}):
                return jsonify(info="Driver with the same name already exist"),400
            driver_data["name"] = driver["driver"]["name"]

        if "phone" in driver["driver"]:
            driver_data["phone"] = driver["driver"]["phone"],

        db.update(table="users", params=driver_data, conditions={"id": id, "type":"driver"})
        return jsonify(info="Driver updated successfully"),200

    else :
        abort(400)


#TODO get customer_id : session dd
@driver_blueprint.route("/drivers/<id>", methods=['DELETE'])
def delete(id:int):
    if not db.is_existing(table="users", conditions={"id":id, "type":"driver"}):
        return jsonify(info="Driver not found"), 404

    db.delete(table="users", conditions={"id":id, "type":"driver"})
    return jsonify(info="Driver deleted successfully"),200



@driver_blueprint.route("/drivers/<id>", methods=['GET'])
def get(id:int):
    if not db.is_existing(table="users", conditions={"id":id, "type":"driver"}):
        return jsonify(info="Driver not found"), 404

    driver = db.select(table="users", conditions={"id":id, "type":"driver"}, multiple=False)
    return jsonify(driver=driver),200


@driver_blueprint.route("/drivers/all", methods=['GET'])
def getAll():
    _SQL = """SELECT users.*,
              locations.lat AS location_lat ,
              locations.lng AS location_lng
              FROM users
              INNER JOIN locations ON users.location_id = locations.id;
              WHERE type=driver
            """

    drivers_raw= db.query(sql=_SQL)

    if len(drivers_raw) <1:
        return jsonify(customers=drivers_raw), 200

    customers = []
    for driver in drivers_raw:
        d = {
            "driver": {
                "id": driver["id"],
                "name": driver["name"],
                "phone": driver["phone"],
                "location": {
                    "lat": driver["location_lat"],
                    "lng": driver["location_lng"],
                }
            }
        }
        customers.append(d)
    return jsonify(customers=customers),200



# @driver_blueprint.route("/drivers/<driverID>/deliveries/<deliveryID>", methods=['PUT'])
# def assign_Delivery(driverID:int, deliveryID:int):
#      if not db.is_existing(table="users", conditions={"id":driverID, "type":"driver"}):
#         return jsonify(info="Driver not found"), 404
#      deliveries.get(deliveryID)




