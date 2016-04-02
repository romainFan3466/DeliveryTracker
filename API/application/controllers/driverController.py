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


@driver_blueprint.route("/api/drivers/<driver_id>/vehicles", methods=['PUT'])
@sessionDecorator.required_user("admin")
def set_vehicle(driver_id:int):

    def reset_vehicle(index, driver_id):
        _sql = """
                  UPDATE vehicles
                  SET vehicles.driver_id = NULL
                  WHERE vehicles.id = (
                    SELECT users.vehicle_id_""" + str(index) +"""
                    FROM users
                    WHERE users.id = %(id)s );
                """
        db.query(_sql, params={"id" : driver_id}, fetch=False)


    company_id = session["user"]["company_id"]
    if not db.is_existing(table="users",conditions={"id":driver_id, "type":"driver", "company_id": company_id}):
        return jsonify(info="Driver not found"), 404

    vehicles = request.get_json(force=True)
    vehicles = Driver.parse(vehicles, "set_vehicle")

    if "errors" in vehicles:
        return jsonify(errors=vehicles["errors"]),400

    vehicles = vehicles["vehicles"]

    for k,v in vehicles.items():

        if v is not None:

            if not db.is_existing(table="vehicles", conditions={"company_id": company_id, "id":v}):
                return jsonify(info="Vehicle " + str(k) + " not found"), 404

            _sql = """ SELECT 1 FROM vehicles WHERE company_id=%(company_id)s AND id= %(v_id)s AND (driver_id IS NULL OR driver_id=%(id)s); """

            # if wished vehicle is available
            if db.query(_sql,params={"company_id" : company_id, "id": driver_id, "v_id" : v}, multiple=False) is not None:

                # reset old vehicle
                reset_vehicle(k[1], driver_id)

                # update vehicle
                db.update(table="vehicles", params={"driver_id": driver_id}, conditions={"id":v})

            else :
                return jsonify(info="Vehicle " + str(k) + " already taken"), 400

        else :
            # reset old vehicle
            reset_vehicle(k[1], driver_id)

        # update user
        db.update(table="users", params={"vehicle_id_"+k[1]: v}, conditions={"id" : driver_id})

    return jsonify(info="Vehicles set successfully"), 200



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


# @sessionDecorator.required_user("admin")
def get_all_drivers(company_id:int, return_obj=False, vehicles=False):
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
    drivers = get_all_drivers(session["user"]["company_id"])
    return jsonify(drivers=drivers),200


@driver_blueprint.route("/api/drivers/location", methods=['PUT'])
@sessionDecorator.required_user("driver")
@locationDecorator.checkLocation()
def updateLocation(lat:int,lng:int):
    driver_id = session["user"]["id"]
    db.update(table="users", params={"location_lat": lat, "location_lng":lng}, conditions={"id": driver_id})
    return jsonify(info="Location successfully updated")





