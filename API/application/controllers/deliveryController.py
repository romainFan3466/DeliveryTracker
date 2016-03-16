from flask import abort, Blueprint, request, jsonify, session, send_file
from application import db, app
from application.classes.Delivery import Delivery
import os
import application.decorators.sessionDecorator as sessionDecorator

delivery_blueprint = Blueprint('delivery', __name__, )

@sessionDecorator.required_user()
def get_all_deliveries(conditions:dict, return_obj=False, get_locations=False):
    conditions = Delivery.parse(conditions, "getAll")
    if "errors" in conditions:
        return jsonify(errors=conditions["errors"]),400

    cond = ""
    conditions = conditions["conditions"] if "conditions" in conditions else conditions

    if "start" in conditions and "end" in conditions:
        cond = "(deliveries.date_due BETWEEN '" + conditions["start"].strftime("%Y-%m-%d %H:%M:%S") + \
                   "' AND '" + conditions["end"].strftime("%Y-%m-%d %H:%M:%S") + "') "

    if "customer_id" in conditions:
        if cond != "":
            cond += " AND "
        cond += "deliveries.customer_id = " + str(conditions["customer_id"])


    if "state" in conditions:
        if cond != "":
            cond += " AND "
        cond += "deliveries.state='" + str(conditions["state"]) +"'"

    if cond != "":
        cond += " AND "

        # Driver session
    cond += "deliveries.company_id=" + str(session["user"]["company_id"]) + " "

    if session["user"]["type"] == "driver":
        cond += "AND deliveries.driver_id=" + str(session["user"]["id"]) + " "


    query = """ SELECT deliveries.* , customers.name AS customer_name"""

    extra_inner = ""
    if get_locations is True:
        query += """ , senders.location_lng as sender_lng,
                  senders.location_lat as sender_lat,
                  receivers.location_lng as receiver_lng,
                  receivers.location_lat as receiver_lat """
        extra_inner = """
          INNER JOIN customers as senders
          ON deliveries.sender_id=senders.id
          INNER JOIN customers as receivers
          ON deliveries.receiver_id=receivers.id
      """

    query+= """ FROM deliveries""" + """
      INNER JOIN customers
      ON deliveries.customer_id=customers.id """ + extra_inner + """
      WHERE """ + cond + " ;"

    deliveries_raw = db.query(query)

    deliveries = []

    if return_obj:
        for delivery in deliveries_raw:
            deliveries.append(Delivery(delivery))

    else :
        for delivery in deliveries_raw:
            d= {"delivery": Delivery(delivery).to_dict()}
            deliveries.append(d)

    return deliveries



@delivery_blueprint.route("/api/deliveries", methods=['POST'])
@sessionDecorator.required_user("admin")
def create():
    args = request.get_json(force=True)
    delivery = Delivery.parse(args, "create")
    if "errors" in delivery:
        return jsonify(errors=delivery["errors"]),400

    delivery = delivery["delivery"]
    delivery["company_id"] = session["user"]["company_id"]

    if not db.is_existing(table="customers", conditions={"id": delivery["customer_id"]}):
        return jsonify(info="Customer not found"), 404

    # check existing customer
    if not db.is_existing(table="customers", conditions={"id": delivery["sender_id"]}):
        return jsonify(info="Sender not found"), 404

    # check existing customer
    if not db.is_existing(table="customers", conditions={"id": delivery["receiver_id"]}):
        return jsonify(info="Receiver not found"), 404

    delivery_id = db.insert(table="deliveries", params=delivery)

    return jsonify(info="Delivery created successfully", deliveryId=delivery_id), 200


@delivery_blueprint.route("/api/deliveries/<id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def update(id: int):
    if not db.is_existing(table="deliveries", conditions={"id": id}):
        return jsonify(info="Delivery not found"), 404
    
    args = request.get_json(force=True)
    delivery = Delivery.parse(args, "update")
    if "errors" in delivery:
        return jsonify(errors=delivery["errors"]),400
    delivery = delivery["delivery"]

    delivery["company_id"] = session["user"]["company_id"]

    # customer_id
    if "customer_id" in delivery:
        if not db.is_existing(table="customers", conditions={"id": delivery["customer_id"]}):
            return jsonify(info="Customer not found"), 404

        # sender_id
    if "sender_id" in delivery:
        if not db.is_existing(table="customers", conditions={"id": delivery["sender_id"]}):
            return jsonify(info="Sender not found"), 404

        # receiver_id
    if "receiver_id" in delivery:
        if not db.is_existing(table="customers", conditions={"id": delivery["receiver_id"]}):
            return jsonify(info="Receiver not found"), 404

    
    db.update(table="deliveries", params=delivery, conditions={"id": id})
    return jsonify(info="Delivery updated successfully"), 200



@delivery_blueprint.route("/api/deliveries/<id>", methods=['DELETE'])
@sessionDecorator.required_user("admin")
def delete(id: int):
    if not db.is_existing(table="deliveries", conditions={"id": id, "company_id": session["user"]["company_id"]}):
        return jsonify(info="Delivery not found"), 404

    db.delete(table="deliveries", conditions={"id": id})
    return jsonify(info="Delivery deleted successfully"), 200


@delivery_blueprint.route("/api/deliveries/<id>", methods=['GET'])
@sessionDecorator.required_user()
def get(id: int):
    conditions = {
        "id": id,
        "company_id": session["user"]["company_id"]
    }

    if session["user"]["type"] == "driver":
        conditions["driver_id"] = session["user"]["id"]

    delivery = db.select(table="deliveries", conditions=conditions, multiple=False)

    if delivery is None:
        return jsonify(info="Delivery not found"), 404

    d= {"delivery": Delivery(delivery).to_dict()}
    return jsonify(delivery=d), 200


@delivery_blueprint.route("/api/deliveries/all", methods=['POST'])
@sessionDecorator.required_user()
def getAll():
    args = request.get_json(force=True)
    deliveries = get_all_deliveries(args)
    #TODO : for driver, send by order closest to farthest
    return jsonify(deliveries=deliveries), 200


@delivery_blueprint.route("/api/deliveries/<delivery_id>/drivers/<driver_id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def assign_driver(delivery_id: int, driver_id: int,):
    company_id = session["user"]["company_id"]
    if not db.is_existing(table="users", conditions={"id": driver_id, "type": "driver", "company_id": company_id}):
        return jsonify(info="Driver not found"), 404

    if not db.is_existing(table="deliveries", conditions={"id": delivery_id, "company_id": company_id}):
        return jsonify(info="Delivery not found"), 404

    db.update(table="deliveries", params={"driver_id": driver_id},
              conditions={"id": delivery_id, "company_id": company_id})
    return jsonify(info="Driver has been assigned"), 200


@delivery_blueprint.route("/api/deliveries/state", methods=['PUT'])
@sessionDecorator.required_user()
def update_state():
    args = request.get_json(force=True)
    req = Delivery.parse(args, "update_state")
    if "errors" in req:
        return jsonify(errors=req["errors"]),400

    state = req["state"]
    conditions = {
        "id": req["delivery_id"],
        "company_id": session["user"]["company_id"]
    }
    supported_states = ["not taken", "taken", "picked up", "on way", "delivered", "canceled"]
    if not state in supported_states:
        return jsonify(info="unsupported states", supported_states=supported_states), 400

    if session["user"]["type"] == "driver":
        conditions["driver_id"] = session["user"]["id"]

    delivery = db.is_existing(table="deliveries", conditions=conditions)

    if not delivery:
        return jsonify(info="Delivery not found"), 404

    if state == "canceled":
        db.update(table="deliveries",params={"canceled" : 1}, conditions=conditions)
    else :
        db.update(table="deliveries",params={"state" : state}, conditions=conditions)

    return jsonify(info="Delivery state has been updated"), 200


@delivery_blueprint.route("/api/deliveries/signature/<delivery_id>", methods=['POST'])
@sessionDecorator.required_user('driver')
def upload_signature(delivery_id):
    conditions = {
            "id": delivery_id,
            "driver_id" : session["user"]["id"],
            "company_id": session["user"]["company_id"]
    }
    if not db.is_existing(table="deliveries", conditions=conditions):
        return jsonify(info="Delivery not found"), 404

    if "file" in request.files:
        file = request.files['file']
        if file.content_type == 'image/png':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], delivery_id+".png"))
            return jsonify(info="ok"), 200
        return jsonify(info="Content type must be 'image/png'"), 400
    abort(400)


@delivery_blueprint.route("/api/deliveries/signature/<delivery_id>", methods=['GET'])
@sessionDecorator.required_user("admin")
def get_signature(delivery_id):
    conditions = {
            "id": delivery_id,
            "company_id": session["user"]["company_id"]
    }
    if not db.is_existing(table="deliveries", conditions=conditions):
        return jsonify(info="Delivery not found"), 404

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], delivery_id+".png")
    if os.path.isfile(file_path):
        return send_file(file_path, "image/png")

    return jsonify(info="Signature not found"), 404
