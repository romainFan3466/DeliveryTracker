from flask import abort, Blueprint, request, jsonify, session, send_file
from application import db, app
from application.classes.Delivery import Delivery
import os
import application.decorators.sessionDecorator as sessionDecorator

delivery_blueprint = Blueprint('delivery', __name__, )


def get_all_deliveries(company_id:int, conditions:dict, return_obj=False, get_locations=False, driver_id:int=None):
    conditions = Delivery.parse(conditions, "getAll")
    if "errors" in conditions:
        return conditions

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
    cond += "deliveries.company_id=" + str(company_id) + " "

    if driver_id is not None:
        cond += "AND deliveries.driver_id=" + str(driver_id) + " "

    query = """ SELECT deliveries.* , delivery_orders.num_order, customers.name AS customer_name"""

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

    query+= """ FROM deliveries
      INNER JOIN customers
      ON deliveries.customer_id=customers.id
      INNER JOIN delivery_orders
      ON deliveries.id=delivery_orders.delivery_id """+ extra_inner + """
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


def insert_at_last_order(delivery_id, date, driver_id):
    last = db.select(table="delivery_orders", selected_columns=("MAX(num_order)",), conditions={"date":date,"driver_id": driver_id}, multiple=False)
    last = last["MAX(num_order)"]+1 if isinstance(last["MAX(num_order)"], int) else 1
    db.insert(table="delivery_orders", params={"num_order": last, "date":date, "delivery_id": delivery_id, "driver_id":driver_id })


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
    d= db.select(table="deliveries", conditions={"id": id}, multiple=False)
    if d is None:
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

    if "date_due" in delivery and d["driver_id"] is not None:
        db.delete(table="delivery_orders", conditions={"delivery_id": id}) # delete old date
        insert_at_last_order(id, delivery["date_due"], d["driver_id"])

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

    d= Delivery(delivery).to_dict()
    return jsonify(delivery=d), 200


@delivery_blueprint.route("/api/deliveries/all", methods=['POST'])
@sessionDecorator.required_user()
def getAll():
    args = request.get_json(force=True)
    company_id = session["user"]["company_id"]
    driver_id = session["user"]["id"] if session["user"]["type"] == "driver" else None
    deliveries = get_all_deliveries(company_id=company_id, conditions=args,driver_id=driver_id, get_locations=True)
    if "errors" in deliveries:
        return jsonify(errors=deliveries),400

    return jsonify(deliveries=deliveries), 200


@delivery_blueprint.route("/api/deliveries/<delivery_id>/drivers/<driver_id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def assign_driver(delivery_id: int, driver_id: int,):
    company_id = session["user"]["company_id"]
    if not db.is_existing(table="users", conditions={"id": driver_id, "type": "driver", "company_id": company_id}):
        return jsonify(info="Driver not found"), 404

    def get_valid_delivery(delivery_id, company_id):
        sql = "SELECT date_due FROM deliveries WHERE id=%(id)s AND company_id=%(company_id)s AND (state='not taken' OR state='not assigned');"
        return db.query(sql, params={"id": delivery_id, "company_id": company_id}, multiple=False)

    delivery = get_valid_delivery(delivery_id, company_id)
    if delivery is None:
        return jsonify(info="Delivery not found or not assignable"), 404

    db.update(table="deliveries", params={"driver_id": driver_id, "state":'not taken'},
              conditions={"id": delivery_id, "company_id": company_id})

    insert_at_last_order(delivery_id, delivery["date_due"] , driver_id)

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
