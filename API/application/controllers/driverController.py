from flask import Blueprint, request, abort, jsonify, session
from application import db
from application.core.generator import Generator
import application.controllers.deliveryController as deliveries
import application.decorators.sessionDecorator as sessionDecorator
import application.decorators.locationDecorator as locationDecorator
from werkzeug.security import generate_password_hash

driver_blueprint = Blueprint('driver', __name__,)

@driver_blueprint.route("/api/drivers", methods=['POST'])
@sessionDecorator.required_user("admin")
def create():
    company_id = session["user"]["company_id"]
    driver = request.get_json(force=True)
    if(
        "driver" in driver and
        "name" in driver["driver"] and
        "email" in driver["driver"] and
        "phone" in driver["driver"]
    ):

        if db.is_existing(table="users",
                          conditions={"name": driver["driver"]["name"], "type":"driver", "company_id":company_id}):
            return jsonify(info="Driver with the same name already exist"),400

        if db.is_existing(table="users",
                          conditions={"email": driver["driver"]["email"], "type":"driver", "company_id": company_id}):
                return jsonify(info="Driver with the same email already exist"),400

        pwd = Generator.password()

        driver_data={
            "name" : driver["driver"]["name"],
            "email" : driver["driver"]["email"],
            "password" : generate_password_hash(pwd),
            "company_id" : company_id,
            "phone" : driver["driver"]["phone"],
            "type":"driver"
        }
        driverId = db.insert(table="users", params=driver_data)
        return jsonify(info="Driver created successfully", driverId=driverId, password=pwd),200
    else :
        abort(400)


@driver_blueprint.route("/api/drivers/<id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def update(id:int):
    company_id = session["user"]["company_id"]
    if not db.is_existing(table="users", conditions={"id":id, "type":"driver", "company_id": company_id}):
        return jsonify(info="Driver not found"), 404

    driver = request.get_json(force=True)
    if "driver" in driver:
        driver_data = {}

        if "name" in driver["driver"]:
            if db.is_existing(table="users",
                          conditions={"name": driver["driver"]["name"], "type":"driver", "company_id": company_id}):
                return jsonify(info="Driver with the same name already exist"),400
            driver_data["name"] = driver["driver"]["name"]

        if "email" in driver["driver"]:
            if db.is_existing(table="users",
                          conditions={"email": driver["driver"]["email"], "type":"driver", "company_id": company_id}):
                return jsonify(info="Driver with the same email already exist"),400
            driver_data["email"] = driver["driver"]["email"]

        if "phone" in driver["driver"]:
            driver_data["phone"] = driver["driver"]["phone"],

        db.update(table="users", params=driver_data, conditions={"id": id})
        return jsonify(info="Driver updated successfully"),200

    else :
        abort(400)


@driver_blueprint.route("/api/drivers/<id>", methods=['DELETE'])
@sessionDecorator.required_user("admin")
def delete(id:int):
    company_id = session["user"]["company_id"]
    if not db.is_existing(table="users", conditions={"id":id, "type":"driver","company_id": company_id}):
        return jsonify(info="Driver not found"), 404

    db.delete(table="users", conditions={"id":id})
    return jsonify(info="Driver deleted successfully"),200


@driver_blueprint.route("/api/drivers/<id>", methods=['GET'])
@sessionDecorator.required_user("admin")
def get(id:int):

    company_id = session["user"]["company_id"]
    d = db.select(table="users", conditions={"id":id, "type":"driver", "company_id": company_id}, multiple=False)

    if d is None:
        return jsonify(info="Driver not found"), 404

    driver = {
        "id": d["id"],
        "name": d["name"],
        "email": d["email"],
        "phone": d["phone"],
        "location": {
            "lat": d["location_lat"],
            "lng": d["location_lng"]
        }
    }
    return jsonify(driver=driver),200


@driver_blueprint.route("/api/drivers/all", methods=['GET'])
@sessionDecorator.required_user("admin")
def getAll():
    company_id = session["user"]["company_id"]
    drivers_raw= db.select(table="users", conditions={"type":"driver", "company_id": company_id}, multiple=True)

    if len(drivers_raw) <1:
        return jsonify(drivers=drivers_raw), 200

    drivers = []
    for driver in drivers_raw:
        d = {
            "driver": {
                "id": driver["id"],
                "name": driver["name"],
                "phone": driver["phone"],
                "email": driver["email"],
                "location": {
                    "lat": driver["location_lat"],
                    "lng": driver["location_lng"],
                }
            }
        }
        drivers.append(d)
    return jsonify(drivers=drivers),200



@driver_blueprint.route("/api/drivers/location", methods=['PUT'])
@sessionDecorator.required_user("driver")
@locationDecorator.checkLocation()
def updateLocation(lat:int,lng:int):
    driver_id = session["user"]["id"]
    db.update(table="users", params={"location_lat": lat, "location_lng":lng}, conditions={"id": driver_id})
    return jsonify(info="Location successfully updated")


@driver_blueprint.route("/api/drivers/<driver_id>/deliveries/<delivery_id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def assign_Delivery(driver_id:int, delivery_id:int):
    company_id = session["user"]["company_id"]
    if not db.is_existing(table="users", conditions={"id":driver_id, "type":"driver", "company_id": company_id}):
       return jsonify(info="Driver not found"), 404

    if not db.is_existing(table="deliveries", conditions={"id": delivery_id, "company_id": company_id}):
        return jsonify(info="Delivery not found"), 404

    db.update(table="deliveries", params={"driver_id": driver_id}, conditions={"id": delivery_id, "company_id": company_id})
    return jsonify(info="Driver has been assigned"), 200






