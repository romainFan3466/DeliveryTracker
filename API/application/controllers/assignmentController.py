from application.classes.Location import Location
from application.controllers.deliveryController import get_all_deliveries
from application.controllers.driverController import get_all_drivers
from application.classes.Driver import Driver
from application.classes.Delivery import Delivery
from flask import jsonify, Blueprint, request, session
import application.decorators.sessionDecorator as sessionDecorator
import datetime

assignment_blueprint= Blueprint('assignment', __name__,)

def is_assignable(driver:Driver, delivery:Delivery):
    vehicles= driver.get_vehicles()
    value = True
    for v in vehicles:
        value = value and (v.get_free_area() >= delivery.get_area()) and (v.get_free_weight() >= delivery.get_weight())

    return False if len(vehicles)== 0 else value


def sort_distances(distances:list):
    sorted = list(distances)
    for i in range(1, len(sorted)):
        j = i
        while j > 0 and sorted[j]["distance"]["distance"] < sorted[j-1]["distance"]["distance"] :
            sorted[j], sorted[j-1]= sorted[j-1], sorted[j]
            j -= 1
    return sorted


def append_suggestion(suggestions:list, driver:Driver, delivery):
    found = False
    for sup in suggestions:
        if "driver" in sup and sup["driver"].get_id() == driver.get_id():
            if not "deliveries" in sup:
                sup["deliveries"] = []
            sup["deliveries"].append(delivery)
            found=True
            break
    if found is False:
        suggestions.append({"driver" : driver, "deliveries":[delivery]})



@sessionDecorator.required_user("admin")
@assignment_blueprint.route("/api/assignment", methods=['POST'])
def suppose_assignment():
    # import all not taken deliveries
    now = datetime.datetime.now()

    cond = {
        "conditions" :  {
            # "start" : datetime.datetime(now.year,now.month,now.day,0,0,0).strftime("%Y-%m-%d %H:%M:%S"),
            # "end" : (datetime.datetime(now.year,now.month,now.day,0,0,0) + datetime.timedelta(days=1, seconds=-1)).strftime("%Y-%m-%d %H:%M:%S"),
            "state" : "not assigned"
        }
    }

    deliveries = get_all_deliveries(company_id=session["user"]["company_id"], conditions=cond , return_obj=True, get_locations=True)

    # import drivers
    drivers = get_all_drivers(session["user"]["company_id"], return_obj=True, vehicles=True)


    suggestions = []
    no_registered = []

    for delivery in deliveries:
        best_distance = None
        best_driver = None

        for driver in drivers:
            if is_assignable(driver, delivery):
                distance = Location.getDistance(delivery.getSenderLocation(), driver.getLocation())
                if best_distance is not None:
                    if distance["distance"]["value"]< best_distance["distance"]["value"] :
                        best_distance = distance
                        best_driver = driver
                else:
                    best_distance = distance
                    best_driver = driver


        if best_distance is None or best_driver is None:
            no_registered.append(delivery)

        else :
            best = {"delivery" : delivery, "distance": best_distance["distance"], "duration" : best_distance["duration"]}
            append_suggestion(suggestions, best_driver, best)

            #update driver position
            best_driver.update_location(**delivery.getSenderLocation())


    return jsonify(suggestions=suggestions),200




