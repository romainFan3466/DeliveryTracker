from flask import abort, Blueprint, request, jsonify, session
from application import db

import application.decorators.sessionDecorator as sessionDecorator
import datetime

delivery_blueprint = Blueprint('delivery', __name__,)

# TODO : implement weight, size, description, type
@delivery_blueprint.route("/api/deliveries", methods=['POST'])
@sessionDecorator.required_user("admin")
def create():
    delivery = request.get_json(force=True)
    if (
        "delivery" in delivery and
        "customer_id" in delivery["delivery"] and
        "date_created" in delivery["delivery"] and
        "weight" in delivery["delivery"] and
        "area" in delivery["delivery"] and
        "content" in delivery["delivery"] and
        "sender_id" in delivery["delivery"] and
        "receiver_id" in delivery["delivery"]
    ):

        # check existing customer
        if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["customer_id"]}) :
            return jsonify(info="Customer not found"),404

        # check existing customer
        if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["sender_id"]}) :
            return jsonify(info="Sender not found"),404

        # check existing customer
        if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["receiver_id"]}) :
            return jsonify(info="Receiver not found"),404


        formatted_delivery ={
            "customer_id" : delivery["delivery"]["customer_id"],
            "sender_id" : delivery["delivery"]["sender_id"],
            "receiver_id" : delivery["delivery"]["receiver_id"],
            "company_id" : session["user"]["company_id"],
            "content" : delivery["delivery"]["content"],
        }

        weight = delivery["delivery"]["weight"]
        area = delivery["delivery"]["area"]

        if (isinstance(area, float) or isinstance(area, int)) and area < 50 and area > 0:
            formatted_delivery["area"] = area
        else:
            abort(400)

        if (isinstance(weight, float) or isinstance(weight, int)) and weight < 36000 and weight > 0:
            formatted_delivery["weight"] = weight
        else:
            abort(400)

        try:
            formatted_delivery["date_created"] = datetime.datetime.strptime(delivery["delivery"]["date_created"],"%Y-%m-%d %H:%M:%S")

            if "date_pickup" in delivery["delivery"]:
                formatted_delivery["date_pickup"] = datetime.datetime.strptime(delivery["delivery"]["date_pickup"],"%Y-%m-%d %H:%M:%S")

            if "date_delivery" in delivery["delivery"]:
                formatted_delivery["date_delivery"] = datetime.datetime.strptime(delivery["delivery"]["date_delivery"],"%Y-%m-%d %H:%M:%S")
        except ValueError:
            abort(400)
            
        if "info" in delivery["delivery"]:
            formatted_delivery["info"] = delivery["delivery"]["info"]

        delivery_id = db.insert(table="deliveries", params=formatted_delivery)

        return jsonify(info="Delivery created successfully", deliveryId=delivery_id),200

    else:
        abort(400)



@delivery_blueprint.route("/api/deliveries/<id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def update(id:int):
    if not db.is_existing(table="deliveries", conditions={"id":id}):
        return jsonify(info="Delivery not found"), 404

    delivery = request.get_json(force=True)

    if "delivery" in delivery:
        formatted_delivery ={
            "company_id" : session["user"]["company_id"]
        }

        #content
        if "content" in delivery["delivery"]:
            formatted_delivery["content"] = delivery["delivery"]["content"]
            
        #info
        if "info" in delivery["delivery"]:
            formatted_delivery["info"] = delivery["delivery"]["info"]
            
        # area
        if "area" in delivery["delivery"]:
            area = delivery["delivery"]["area"]
            if (isinstance(area, float) or isinstance(area, int)) and area < 50 and area > 0:
                formatted_delivery["area"] = area
            else:
                abort(400)

        #weight
        if "weight" in delivery["delivery"]:
            weight = delivery["delivery"]["weight"]
            if (isinstance(weight, float) or isinstance(weight, int)) and weight < 36000 and weight > 0:
                formatted_delivery["weight"] = weight
            else:
                abort(400)
        
        #customer_id
        if "customer_id" in delivery["delivery"]:
            if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["customer_id"]}):
                return jsonify(info="Customer not found"), 404
            formatted_delivery["customer_id"] = delivery["delivery"]["customer_id"]

         #sender_id
        if "sender_id" in delivery["delivery"]:
            if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["sender_id"]}):
                return jsonify(info="Sender not found"), 404
            formatted_delivery["sender_id"] = delivery["delivery"]["sender_id"]

         #receiver_id
        if "receiver_id" in delivery["delivery"]:
            if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["receiver_id"]}):
                return jsonify(info="Receiver not found"), 404
            formatted_delivery["receiver_id"] = delivery["delivery"]["receiver_id"]

        #date
        try:
            if "date_pickup" in delivery["delivery"]:
                formatted_delivery["date_pickup"] = datetime.datetime.strptime(delivery["delivery"]["date_pickup"],
                                                                               "%Y-%m-%d %H:%M:%S")

            if "date_delivery" in delivery["delivery"]:
                formatted_delivery["date_delivery"] = datetime.datetime.strptime(delivery["delivery"]["date_delivery"],
                                                                                 "%Y-%m-%d %H:%M:%S")
        except ValueError:
            abort(400)

        db.update(table="deliveries", params=formatted_delivery, conditions={"id": id})
        return jsonify(info="Delivery updated successfully"), 200
    else :
        abort(400)



@delivery_blueprint.route("/api/deliveries/<id>", methods=['DELETE'])
@sessionDecorator.required_user("admin")
def delete(id:int):
    if not db.is_existing(table="deliveries", conditions={"id":id, "company_id" : session["user"]["company_id"]}):
        return jsonify(info="Delivery not found"), 404

    db.delete(table="deliveries", conditions={"id":id})
    return jsonify(info="Delivery deleted successfully"),200



@delivery_blueprint.route("/api/deliveries/<id>", methods=['GET'])
@sessionDecorator.required_user("admin")
def get(id:int):

    delivery=db.select(table="deliveries", conditions={"id": id, "company_id" : session["user"]["company_id"]}, multiple=False)

    if delivery is None:
        return jsonify(info="Delivery not found"), 404

    d = {
        "id": delivery["id"],
        "customer_id": delivery["customer_id"],
        "sender_id": delivery["sender_id"],
        "receiver_id": delivery["receiver_id"],
        "weight": delivery["weight"],
        "area": delivery["area"],
        "content": delivery["content"],
        "info": delivery["info"],
        "driver_id": delivery["driver_id"],
        "date_pickup": delivery["date_pickup"],
        "date_delivery": delivery["date_delivery"],
        "date_created": delivery["date_created"],
    }
    return jsonify(delivery=d), 200



@delivery_blueprint.route("/api/deliveries/all", methods=['GET'])
@sessionDecorator.required_user("admin")
def getAll():

    deliveries_raw=db.select(table="deliveries", conditions={"company_id" : session["user"]["company_id"]})

    if len(deliveries_raw) <1:
        return jsonify(deliveries=[]), 200

    deliveries = []

    for delivery in deliveries_raw:
        d = {
            "delivery" : {
                "id" : delivery["id"],
                "customer_id": delivery["customer_id"],
                "sender_id": delivery["sender_id"],
                "receiver_id": delivery["receiver_id"],
                "weight": delivery["weight"],
                "area": delivery["area"],
                "content": delivery["content"],
                "info": delivery["info"],
                "driver_id" : delivery["driver_id"],
                "date_pickup" : delivery["date_pickup"],
                "date_delivery" : delivery["date_delivery"],
                "date_created" : delivery["date_created"],
            }
        }
        deliveries.append(d)

    return jsonify(deliveries=deliveries), 200

