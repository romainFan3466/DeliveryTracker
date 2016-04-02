from flask import abort, Blueprint, request, jsonify, session, send_file
from application import db, app
from application.classes.Delivery import Delivery
import os, random
import application.decorators.sessionDecorator as sessionDecorator
from application.controllers.deliveryController import assign_driver, update_state

mock_blueprint = Blueprint('mockData', __name__, )


@mock_blueprint.route("/api/generateRandomDelivery", methods=['POST'])
@sessionDecorator.required_user("admin")
def generate_random():

    req = request.get_json(force=True)
    company_id = session["user"]["company_id"]

    list_content = ["fish", "glass", "vegetables", "fragile", "frozen", "wood", "letter", "material", "electronic"]

    random_weight = lambda : round(random.uniform(0.10, 2000.00),2)
    random_area = lambda : round(random.uniform(0.10, 34.00), 2)

    customer_ids = db.select(table="customers", selected_columns=("id",), conditions={"company_id" : company_id}, multiple=True)

    random_receiver  = lambda id : random.choice([v["id"] for v in customer_ids if v["id"]!=id ])

    for x in range(0, 5):
        delivery = {
            "customer_id" : random.choice(customer_ids)["id"],
            "sender_id" : random.choice(customer_ids)["id"],
            "date_due" : req["date_due"],
            "date_created" : req["date_due"],
            "content" : random.choice(list_content),
            "area" : random_area(),
            "weight" : random_weight(),
            "company_id" : company_id
        }

        delivery["receiver_id"] = random_receiver(delivery["sender_id"])
        er = 3
        delivery_id = db.insert(table="deliveries", params=delivery)
        assign_driver(delivery_id, 3)

        # if x <3 :
        #     db.update(table="deliveries",params={"state" : "taken"}, conditions={"id": delivery_id, "company_id": company_id})
        #
        # if x>=3 and x<5:
        #     db.update(table="deliveries",params={"state" : "on way"}, conditions={"id": delivery_id, "company_id": company_id})
        #
        # if x==7 :
        #     db.update(table="deliveries",params={"state" : "picked up"}, conditions={"id": delivery_id, "company_id": company_id})
        #
        # if x==8 :
        #     db.update(table="deliveries",params={"state" : "delivered"}, conditions={"id": delivery_id, "company_id": company_id})


    return jsonify(info="done"), 200






