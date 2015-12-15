from flask import abort, Blueprint, request, jsonify, session
from application import db
from application.classes.Location import Location

import application.decorators.sessionDecorator as sessionDecorator
import datetime

delivery_blueprint = Blueprint('delivery', __name__,)


@delivery_blueprint.route("/deliveries", methods=['POST'])
@sessionDecorator.required_user("admin")
def create():
    delivery = request.get_json(force=True)
    if (
        "delivery" in delivery and
        "location_delivery" in delivery["delivery"] and
        "location_pickup" in delivery["delivery"] and
        "customer_id" in delivery["delivery"] and
        "date_created" in delivery["delivery"]and
        "lat" in delivery["delivery"]["location_delivery"] and
        "lng" in delivery["delivery"]["location_delivery"] and
        "lat" in delivery["delivery"]["location_pickup"] and
        "lng" in delivery["delivery"]["location_pickup"] and
        Location.isValid(delivery["delivery"]["location_delivery"]["lat"], delivery["delivery"]["location_delivery"]["lng"]) and
        Location.isValid(delivery["delivery"]["location_pickup"]["lat"], delivery["delivery"]["location_pickup"]["lng"])
    ):

        # check existing customer
        if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["customer_id"]}) :
            return jsonify(info="Customer not found"),404


        formatted_delivery ={
            "location_delivery_lat" : delivery["delivery"]["location_delivery"]["lat"],
            "location_delivery_lng" : delivery["delivery"]["location_delivery"]["lng"],
            "location_pickup_lat" : delivery["delivery"]["location_pickup"]["lat"],
            "location_pickup_lng" : delivery["delivery"]["location_pickup"]["lng"],
            "customer_id" : delivery["delivery"]["customer_id"],
            "company_id" : session["user"]["company_id"]
        }

        try:
            formatted_delivery["date_created"] = datetime.datetime.strptime(delivery["delivery"]["date_created"],"%Y-%m-%d %H:%M:%S")

            if "date_pickup" in delivery["delivery"]:
                formatted_delivery["date_pickup"] = datetime.datetime.strptime(delivery["delivery"]["date_pickup"],"%Y-%m-%d %H:%M:%S")

            if "date_delivery" in delivery["delivery"]:
                formatted_delivery["date_delivery"] = datetime.datetime.strptime(delivery["delivery"]["date_delivery"],"%Y-%m-%d %H:%M:%S")
        except ValueError:
            abort(400)

        delivery_id = db.insert(table="deliveries", params=formatted_delivery)

        return jsonify(info="Delivery created successfully", deliveryId=delivery_id),200

    else:
        abort(400)



@delivery_blueprint.route("/deliveries/<id>", methods=['PUT'])
@sessionDecorator.required_user("admin")
def update(id:int):
    if not db.is_existing(table="deliveries", conditions={"id":id}):
        return jsonify(info="Delivery not found"), 404

    delivery = request.get_json(force=True)

    if "delivery" in delivery:
        formatted_delivery ={
            "company_id" : session["user"]["company_id"]
        }

        #customer_id
        if "customer_id" in delivery["delivery"]:
            if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["customer_id"]}):
                return jsonify(info="Customer not found"), 404
            formatted_delivery["customer_id"] = delivery["delivery"]["customer_id"]

        #location pickup
        if "location_pickup" in delivery["delivery"]:
            if (
                "lat" in delivery["delivery"]["location_pickup"] and
                "lng" in delivery["delivery"]["location_pickup"] and
                Location.isValid(delivery["delivery"]["location_pickup"]["lat"], delivery["delivery"]["location_pickup"]["lng"])
            ):
                formatted_delivery["location_pickup_lat"]= delivery["delivery"]["location_pickup"]["lat"]
                formatted_delivery["location_pickup_lng"]= delivery["delivery"]["location_pickup"]["lng"]
            else:
                abort(400)

        #location delivery
        if "location_delivery" in delivery["delivery"]:
            if (
                "lat" in delivery["delivery"]["location_delivery"] and
                "lng" in delivery["delivery"]["location_delivery"] and
                Location.isValid(delivery["delivery"]["location_delivery"]["lat"], delivery["delivery"]["location_delivery"]["lng"])
            ):
                formatted_delivery["location_delivery_lat"] = delivery["delivery"]["location_delivery"]["lat"]
                formatted_delivery["location_delivery_lng"] = delivery["delivery"]["location_delivery"]["lng"]
            else:
                abort(400)

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



@delivery_blueprint.route("/deliveries/<id>", methods=['DELETE'])
@sessionDecorator.required_user("admin")
def delete(id:int):
    if not db.is_existing(table="deliveries", conditions={"id":id, "company_id" : session["user"]["company_id"]}):
        return jsonify(info="Delivery not found"), 404

    db.delete(table="deliveries", conditions={"id":id})
    return jsonify(info="Delivery deleted successfully"),200



@delivery_blueprint.route("/deliveries/<id>", methods=['GET'])
@sessionDecorator.required_user("admin")
def get(id:int):

    delivery=db.select(table="deliveries", conditions={"id": id, "company_id" : session["user"]["company_id"]}, multiple=False)

    if delivery is None:
        return jsonify(info="Delivery not found"), 404

    d = {
        "id": delivery["id"],
        "customer_id": delivery["customer_id"],
        "driver_id": delivery["driver_id"],
        "date_pickup": delivery["date_pickup"],
        "date_delivery": delivery["date_delivery"],
        "date_created": delivery["date_created"],
        "location_pickup": {
            "lat": delivery["location_pickup_lat"],
            "lng": delivery["location_pickup_lng"]
        },
        "location_delivery": {
            "lat": delivery["location_delivery_lat"],
            "lng": delivery["location_delivery_lng"]
        }
    }
    return jsonify(delivery=d), 200



@delivery_blueprint.route("/deliveries/all", methods=['GET'])
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
                "customer_id" : delivery["customer_id"],
                "driver_id" : delivery["driver_id"],
                "date_pickup" : delivery["date_pickup"],
                "date_delivery" : delivery["date_delivery"],
                "date_created" : delivery["date_created"],
                "location_pickup" : {
                    "lat" : delivery["location_pickup_lat"],
                    "lng" : delivery["location_pickup_lng"]
                },
                "location_delivery" : {
                    "lat" : delivery["location_delivery_lat"],
                    "lng" : delivery["location_delivery_lng"]
                }
            }
        }
        deliveries.append(d)

    return jsonify(deliveries=deliveries), 200

