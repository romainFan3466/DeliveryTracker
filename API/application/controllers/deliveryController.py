from flask import abort, Blueprint, request, jsonify
from application import db
from application.classes.Location import Location


delivery_blueprint = Blueprint('delivery', __name__,)


@delivery_blueprint.route("/deliveries", methods=['POST'])
def create():
    delivery = request.get_json(force=True)
    if (
        "delivery" in delivery and
        "location_delivery" in delivery["delivery"] and
        "location_pickup" in delivery["delivery"] and
        "customer_id" in delivery["delivery"] and
        "date_created" in delivery["delivery"]and
        ("lat" and "lng" in delivery["delivery"]["location_delivery"]) and
        ("lat" and "lng" in delivery["delivery"]["location_pickup"])
    ):

        # record locations
        location_delivery_id= Location.getIdFromDB(dbInstance=db,
                                                   lat=delivery["delivery"]["location_delivery"]["lat"],
                                                   lng=delivery["delivery"]["location_delivery"]["lng"])

        location_pickup_id= Location.getIdFromDB(dbInstance=db,
                                                   lat=delivery["delivery"]["location_pickup"]["lat"],
                                                   lng=delivery["delivery"]["location_pickup"]["lng"])

        # check existing customer
        if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["customer_id"]}) :
            return jsonify(info="Customer not found"),404

        formatted_delivery ={}
        formatted_delivery["location_delivery_id"] = location_delivery_id
        formatted_delivery["location_pickup_id"] = location_pickup_id
        formatted_delivery["customer_id"] = delivery["delivery"]["customer_id"]
        formatted_delivery["date_created"] = delivery["delivery"]["date_created"]

        if "date_pickup" in delivery["delivery"]:
            formatted_delivery["date_pickup"] = delivery["delivery"]["date_pickup"]

        if "date_delivery" in delivery["delivery"]:
            formatted_delivery["date_delivery"] = delivery["delivery"]["date_delivery"]

        delivery_id = db.insert(table="deliveries", params=formatted_delivery )

        return jsonify(info="Delivery created successfully", deliveryId=delivery_id),200

    else:
        abort(400)



@delivery_blueprint.route("/deliveries/<id>", methods=['PUT'])
def update(id:int):
    if not db.is_existing(table="deliveries", conditions={"id":id}):
        return jsonify(info="Delivery not found"), 404

    delivery = request.get_json(force=True)

    if "delivery" in delivery:
        formatted_delivery ={}

        #customer_id
        if "customer_id" in delivery["delivery"]:
            if not db.is_existing(table="customers", conditions={"id": delivery["delivery"]["customer_id"]}):
                return jsonify(info="Customer not found"), 404
            formatted_delivery["customer_id"] = delivery["delivery"]["customer_id"]

        #location pickup
        if "location_pickup" in delivery["delivery"]:
            if "lat" in delivery["delivery"]["location_pickup"] and "lng" in delivery["delivery"]["location_pickup"]:
                formatted_delivery["location_pickup_id"]= Location.getIdFromDB(dbInstance=db,
                                                         lat=delivery["delivery"]["location_pickup"]["lat"],
                                                         lng=delivery["delivery"]["location_pickup"]["lng"])
        #location delivery
        if "location_delivery" in delivery["delivery"]:
            if "lat" in delivery["delivery"]["location_delivery"] and "lng" in delivery["delivery"]["location_delivery"]:
                formatted_delivery["location_delivery_id"] = Location.getIdFromDB(dbInstance=db,
                                                             lat=delivery["delivery"]["location_delivery"]["lat"],
                                                             lng=delivery["delivery"]["location_delivery"]["lng"])
        #date
        if "date_pickup" in delivery["delivery"]:
            formatted_delivery["date_pickup"] = delivery["delivery"]["date_pickup"]

        if "date_delivery" in delivery["delivery"]:
            formatted_delivery["date_delivery"] = delivery["delivery"]["date_delivery"]

        db.update(table="deliveries", params=formatted_delivery, conditions={"id": id})
        return jsonify(info="Delivery updated successfully"), 200
    else :
        abort(400)



@delivery_blueprint.route("/deliveries/<id>", methods=['DELETE'])
def delete(id:int):
    if not db.is_existing(table="deliveries", conditions={"id":id}):
        return jsonify(info="Delivery not found"), 404

    db.delete(table="deliveries", conditions={"id":id})
    return jsonify(info="Delivery deleted successfully"),200



@delivery_blueprint.route("/deliveries/<id>", methods=['GET'])
def get(id:int):

    _SQL = """SELECT deliveries.*,
            pickup.lat AS location_pickup_lat ,
            pickup.lng AS location_pickup_lng,
            delivery.lat AS location_delivery_lat ,
            delivery.lng AS location_delivery_lng

            FROM deliveries
            INNER JOIN locations AS pickup ON deliveries.location_pickup_id = pickup.id
            INNER JOIN locations AS delivery ON deliveries.location_delivery_id = delivery.id
            WHERE deliveries.id = %(id)s;
          """

    delivery=db.query(_SQL, {"id": id}, multiple=False)

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
            "lng": delivery["location_pickup_lng"],
        },
        "location_delivery": {
            "lat": delivery["location_delivery_lat"],
            "lng": delivery["location_delivery_lng"],
        }
    }
    return jsonify(delivery=d), 200



@delivery_blueprint.route("/deliveries/all", methods=['GET'])
def getAll():

    _SQL = """ SELECT deliveries.*,
            pickup.lat AS location_pickup_lat ,
            pickup.lng AS location_pickup_lng,
            delivery.lat AS location_delivery_lat ,
            delivery.lng AS location_delivery_lng

            FROM deliveries
            INNER JOIN locations AS pickup ON deliveries.location_pickup_id = pickup.id
            INNER JOIN locations AS delivery ON deliveries.location_delivery_id = delivery.id;
          """

    deliveries_raw = db.query(_SQL)

    if len(deliveries_raw) <1:
        return jsonify(deliveries=deliveries_raw), 200

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
                    "lng" : delivery["location_pickup_lng"],
                },
                "location_delivery" : {
                    "lat" : delivery["location_delivery_lat"],
                    "lng" : delivery["location_delivery_lng"],
                }
            }
        }
        deliveries.append(d)

    return jsonify(deliveries=deliveries), 200

