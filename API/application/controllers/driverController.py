from flask import Blueprint, request, abort, jsonify, session
from application import db
from application.core.generator import Generator
import application.decorators.sessionDecorator as sessionDecorator
import application.decorators.locationDecorator as locationDecorator
from werkzeug.security import generate_password_hash
from application.classes.Driver import Driver

driver_blueprint = Blueprint('driver', __name__,)

@driver_blueprint.route("/api/drivers", methods=['POST'])
@sessionDecorator.required_user("admin")
def create():
    company_id = session["user"]["company_id"]
    driver = request.get_json(force=True)
    driver = Driver.parse(driver, "create")
    
    if "errors" in driver:
        return jsonify(errors=driver["errors"]),400
    driver = driver["driver"]

    if db.is_existing(table="users",
                      conditions={"name": driver["name"], "type":"driver", "company_id":company_id}):
        return jsonify(info="Driver with the same name already exist"),400

    if db.is_existing(table="users",
                      conditions={"email": driver["email"], "type":"driver", "company_id": company_id}):
            return jsonify(info="Driver with the same email already exist"),400

    pwd = Generator.password()

    driver_data={
        "name" : driver["name"],
        "email" : driver["email"],
        "password" : generate_password_hash(pwd),
        "company_id" : company_id,
        "phone" : driver["phone"],
        "type":"driver"
    }
    driverId = db.insert(table="users", params=driver_data)
    return jsonify(info="Driver created successfully", driverId=driverId, password=pwd),200
   

@driver_blueprint.route("/api/drivers/<id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def update(id:int):
    company_id = session["user"]["company_id"]
    if not db.is_existing(table="users", conditions={"id":id, "type":"driver", "company_id": company_id}):
        return jsonify(info="Driver not found"), 404

    driver = request.get_json(force=True)
    driver = Driver.parse(driver, "update")
    
    if "errors" in driver:
        return jsonify(errors=driver["errors"]),400
    driver = driver["driver"]
    driver_data = {}

    if "name" in driver:
        if db.is_existing(table="users",
                      conditions={"name": driver["name"], "type":"driver", "company_id": company_id}):
            return jsonify(info="Driver with the same name already exist"),400
        driver_data["name"] = driver["name"]

    if "email" in driver:
        if db.is_existing(table="users",
                      conditions={"email": driver["email"], "type":"driver", "company_id": company_id}):
            return jsonify(info="Driver with the same email already exist"),400
        driver_data["email"] = driver["email"]

    if "phone" in driver:
        driver_data["phone"] = driver["phone"]

    db.update(table="users", params=driver_data, conditions={"id": id})
    return jsonify(info="Driver updated successfully"),200


@driver_blueprint.route("/api/drivers/<driver_id>/vehicles/1/<vehicle1_id>", methods=['PUT'])
@driver_blueprint.route("/api/drivers/<driver_id>/vehicles/1/<vehicle1_id>/2/<vehicle2_id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def set_vehicle(driver_id:int, vehicle1_id:int, vehicle2_id:int=None):
    company_id = session["user"]["company_id"]
    driver = db.select(table="users", selected_columns=("id","vehicle_id_1","vehicle_id_2"),
                     conditions={"id":driver_id, "type":"driver", "company_id": company_id}, multiple=False)
    if driver is None:
        return jsonify(info="Driver not found"), 404

    assigned_vehicle1_by = db.select(table="vehicles", selected_columns=("id","driver_id"), conditions={"id":vehicle1_id, "company_id": company_id}, multiple=False)
    driver_vehicles = [driver["vehicle_id_1"], driver["vehicle_id_2"]]
    assigned_vehicle = []
    assigned_vehicle.append(assigned_vehicle1_by)
    if vehicle2_id is not None:
        assigned_vehicle2_by = db.select(table="vehicles", selected_columns=("id","driver_id"), conditions={"id":vehicle2_id, "company_id": company_id}, multiple=False)
        assigned_vehicle.append(assigned_vehicle2_by)

    for i, v in enumerate(assigned_vehicle, start=1):

        if "driver_id" in v and v["driver_id"] != "" and v["driver_id"] is not None and not v["id"] in driver_vehicles:
            return jsonify(info="Vehicle with id: "+ str(v["id"]) + " already taken"), 404
        else:
            if "vehicle_id_"+str(i) in driver:
                db.update(table="vehicles", params={"driver_id": None }, conditions={"id": driver["vehicle_id_"+str(i)]})

            db.update(table="vehicles", params={"driver_id": driver_id}, conditions={"id": v["id"]})
            db.update(table="users", conditions={"id":driver_id, "type":"driver", "company_id": company_id},
                      params={"vehicle_id_"+str(i): v["id"]})

    return jsonify(info="Driver updated successfully"),200


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
        },
        "vehicle_id_1":d["vehicle_id_1"],
        "vehicle_id_2":d["vehicle_id_2"]
    }
    return jsonify(driver=driver),200


@sessionDecorator.required_user("admin")
def get_all_drivers(return_obj=False, vehicles=False):
    _sql = """
            select users.id,
            users.name,
            users.location_lat,
            users.location_lng,
            users.vehicle_id_1,
            users.vehicle_id_2,
         v1.max_area AS v1_max_area,
         v1.max_weight AS v1_max_weight,
         v1.area AS v1_area,
         v1.weight AS v1_weight,
         v2.max_area AS v2_max_area,
         v2.max_weight AS v2_max_weight,
         v2.area AS v2_area,
         v2.weight AS v2_weight
         from users
        INNER JOIN vehicles AS v1
        ON users.vehicle_id_1 = v1.id
        LEFT JOIN vehicles AS v2
        ON users.vehicle_id_2 = v2.id
        WHERE users.type='driver' and users.company_id = %(company_id)s ;
        """
    company_id = session["user"]["company_id"]
    if vehicles is True:
        drivers_raw = db.query(_sql, {"company_id" : company_id}, multiple=True)
    else :
        drivers_raw= db.select(table="users", conditions={"type":"driver", "company_id": company_id}, multiple=True)

    drivers = []
    if return_obj:
        for driver in drivers_raw:
            drivers.append(Driver(driver))

    else :
        for driver in drivers_raw:
            d = {"driver": Driver(driver).__dict__}
            drivers.append(d)

    return drivers


@driver_blueprint.route("/api/drivers/all", methods=['GET'])
@sessionDecorator.required_user("admin")
def getAll(return_obj=False):
    drivers = get_all_drivers()
    return jsonify(drivers=drivers),200


@driver_blueprint.route("/api/drivers/location", methods=['PUT'])
@sessionDecorator.required_user("driver")
@locationDecorator.checkLocation()
def updateLocation(lat:int,lng:int):
    driver_id = session["user"]["id"]
    db.update(table="users", params={"location_lat": lat, "location_lng":lng}, conditions={"id": driver_id})
    return jsonify(info="Location successfully updated")





