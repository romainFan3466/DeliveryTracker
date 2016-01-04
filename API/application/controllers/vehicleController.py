from flask import Blueprint, session, request, abort, jsonify
from application import db
import application.decorators.sessionDecorator as sessionDecorator
vehicle_blueprint = Blueprint('vehicle', __name__,)


@vehicle_blueprint.route("/api/vehicles", methods=['POST'])
@sessionDecorator.required_user("admin")
def create():
    company_id = session["user"]["company_id"]
    rq = request.get_json(force=True)
    if(
        "vehicle" in rq and
        "registration" in rq["vehicle"] and
        "type" in rq["vehicle"] and
        "max_weight" in rq["vehicle"] and
        "max_area" in rq["vehicle"] and
        (isinstance(rq["vehicle"]["max_area"], float) or isinstance(rq["vehicle"]["max_area"], int)) and
        (isinstance(rq["vehicle"]["max_weight"], float) or isinstance(rq["vehicle"]["max_weight"], int))
    ):
        if db.is_existing(table="vehicles",
                          conditions={"registration": rq["vehicle"]["registration"] ,"company_id": company_id}):
            return jsonify(info="Vehicle with the same registration already exist"), 400

        vehicle_data = {
            "registration" : rq["vehicle"]["registration"],
            "type" : rq["vehicle"]["type"],
            "max_weight" : rq["vehicle"]["max_weight"],
            "max_area" : rq["vehicle"]["max_area"],
            "company_id" : company_id
        }

        vehicle_id = db.insert(table="vehicles", params=vehicle_data)
        return jsonify(info="Vehicle created successfully", vehicleId=vehicle_id)
    else :
        abort(400)



@vehicle_blueprint.route("/api/vehicles/<id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def update(id:int):
    company_id = session["user"]["company_id"]

    if not db.is_existing(table="vehicles", conditions={"id":id, "company_id": company_id}):
         return jsonify(info="Vehicle not found"), 404

    rq = request.get_json(force=True)

    if "vehicle" in rq :
        vehicle_data = {}

        if "registration" in rq["vehicle"]:
            if db.is_existing(table="vehicles",
                          conditions={"registration": rq["vehicle"]["registration"] ,"company_id": company_id}):
                return jsonify(info="Vehicle with the same registration already exist"), 400
            vehicle_data["registration"] = rq["vehicle"]["registration"]

        if "type" in rq["vehicle"]:
            vehicle_data["type"] = rq["vehicle"]["type"]

        if "max_weight" in rq["vehicle"]:
            max_weight = rq["vehicle"]["max_weight"]
            if not (isinstance(max_weight, float) or isinstance(max_weight, int)) or max_weight>100000 or max_weight<0:
                abort(400)
            vehicle_data["max_weight"] = rq["vehicle"]["max_weight"]

        if "max_area" in rq["vehicle"]:
            max_area = rq["vehicle"]["max_area"]
            if not (isinstance(max_area, float) or isinstance(max_area, int)) or max_area>150 or max_area<0:
                abort(400)
            vehicle_data["max_area"] = rq["vehicle"]["max_area"]

        db.update(table="vehicles", params=vehicle_data, conditions={"id": id})
        return jsonify(info="Vehicle updated successfully"),200
    else :
        abort(400)


@vehicle_blueprint.route("/api/vehicles/<id>", methods=['DELETE'])
@sessionDecorator.required_user("admin")
def delete(id:int):
    company_id = session["user"]["company_id"]
    if not db.is_existing(table="vehicles", conditions={"id":id, "company_id": company_id}):
        return jsonify(info="Vehicle not found"), 404

    db.delete(table="vehicles", conditions={"id":id})
    return jsonify(info="Vehicle deleted successfully"),200


@vehicle_blueprint.route("/api/vehicles/<id>", methods=['GET'])
@sessionDecorator.required_user("admin")
def get(id:int):
    company_id = session["user"]["company_id"]
    v = db.select(table="vehicles", conditions={"id":id, "company_id": company_id}, multiple=False)

    if v is None:
        return jsonify(info="Vehicle not found"), 404

    vehicle = {
        "id" : v["id"],
        "registration": v["registration"],
        "type": v["type"],
        "weight": v["weight"],
        "max_weight": v["max_weight"],
        "area": v["area"],
        "max_area": v["max_area"],
    }

    return jsonify(vehicle=vehicle),200


@vehicle_blueprint.route("/api/vehicles/all", methods=['GET'])
@sessionDecorator.required_user("admin")
def getAll():
    company_id = session["user"]["company_id"]
    vs = db.select(table="vehicles", conditions={"company_id": company_id})

    if len(vs) <1:
        return jsonify(vehicles=[]), 200

    vehicles = []

    for v in vs:
        vehicle = {
            "vehicle": {
                "id" : v["id"],
                "registration": v["registration"],
                "type": v["type"],
                "weight": v["weight"],
                "max_weight": v["max_weight"],
                "area": v["area"],
                "max_area": v["max_area"],
            }
        }
        vehicles.append(vehicle)

    return jsonify(vehicles=vehicles), 200
