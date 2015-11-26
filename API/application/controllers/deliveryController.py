from flask import render_template, Blueprint, url_for, redirect, flash, request
from application import db


delivery_blueprint = Blueprint('delivery', __name__,)


@delivery_blueprint.route("/deliveries", methods=['POST'])
def create():
    ID = ""
    date_created = ""
    date_pickup = ""
    date_delivery = ""

    Location_delivery = ""
    Location_pickup = ""

    customer_ID = ""
    driver_ID = ""

    delivery = request.get_json(force=True)

    if (
        "delivery" in delivery["delivery"] and
        "location_delivery" in delivery["delivery"] and
        "location_pickup" in delivery["delivery"] and
        "customer_ID" in delivery["delivery"] and
        "driver_ID" in delivery["delivery"]and
        "date_created" in delivery["delivery"]and
        ("lat" and "lng" in delivery["delivery"]["location_delivery"]) and
        ("lat" and "lng" in delivery["delivery"]["location_pickup"])
    ):

        # record locations
        loc_delivery_ID= db.select(table="locations",
                                   selected_columns=("id",),
                                   conditions=delivery["delivery"]["location_delivery"],
                                   multiple=False)

        loc_pickup_ID= db.select(table="locations",
                                   selected_columns=("id",),
                                   conditions=delivery["delivery"]["location_pickup"],
                                   multiple=False)


        if loc_delivery_ID is None:
            loc_delivery_ID=db.insert(table="locations", params=delivery["delivery"]["location_delivery"])

        if loc_pickup_ID is None:
            loc_pickup_ID=db.insert(table="locations", params=delivery["delivery"]["location_pickup"])

        # record delivery

        # db.insert(table="deliveries", params )

        data={
            ""
        }

    else:
        pass



@delivery_blueprint.route("/deliveries/<id>", methods=['PUT'])
def update(id:int):
    pass


@delivery_blueprint.route("/deliveries/<id>", methods=['DELETE'])
def delete(id:int):
    pass


@delivery_blueprint.route("/deliveries/<id>", methods=['GET'])
def get(id:int):
    pass


@delivery_blueprint.route("/deliveries/all", methods=['GET'])
def getAll():
    pass
