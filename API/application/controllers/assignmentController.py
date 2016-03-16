from application.classes.Location import Location
from application.controllers.deliveryController import get_all_deliveries
from application.controllers.driverController import get_all_drivers
from application.classes.Driver import Driver
from application.classes.Delivery import Delivery
from flask import jsonify, Blueprint, request
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


@sessionDecorator.required_user("admin")
@assignment_blueprint.route("/api/assignment", methods=['POST'])
def suppose_assignment():
    # import all not taken deliveries
    now = datetime.datetime.now()

    cond = {
        "conditions" :  {
            # "start" : datetime.datetime(now.year,now.month,now.day,0,0,0).strftime("%Y-%m-%d %H:%M:%S"),
            # "end" : (datetime.datetime(now.year,now.month,now.day,0,0,0) + datetime.timedelta(days=1, seconds=-1)).strftime("%Y-%m-%d %H:%M:%S"),
            "state" : "not taken"
        }
    }

    deliveries = get_all_deliveries(cond , return_obj=True, get_locations=True)

    # import drivers
    drivers = get_all_drivers(return_obj=True, vehicles=True)


    carlow = { "lat":52.835289, "lng" : -6.925577}
    dublin = { "lat":53.292133, "lng" : -6.245915}

    distance = Location.getDistance(carlow, dublin)


    supposition = {}
    maps = []
    no_registered = []

    for delivery in deliveries:
        best_distance = None
        best_driver = None

        for driver in drivers:
            if is_assignable(driver, delivery):
                distance = Location.getDistance(delivery.getSenderLocation(), driver.getLocation())
                if best_distance is not None:
                    if distance["distance"]< best_distance["distance"] :
                        best_distance = distance
                        best_driver = driver
                else:
                    best_distance = distance
                    best_driver = driver


        if best_distance is None or best_driver is None:
            no_registered.append(delivery)

        else :
            best = {"delivery" : delivery, "distance": best_distance}

            if not str(best_driver) in supposition:
                    supposition[str(best_driver)] = []
            supposition[str(best_driver)].append(best)

            #update driver position
            best_driver.update_location(**delivery.getSenderLocation())


    #### ALGO ####
    ## assign closest and available



    #
    # supposition = {}
    #
    # for node in maps:
    #     sorted = sort_distances(node["distances"])
    #
    #     for driver in sorted:
    #         if is_assignable(driver["driver"], node["delivery"]):
    #             best = {"delivery" : node["delivery"], "driver" : driver["driver"], "distance": driver["distance"]}
    #
    #             if not str(driver["driver"]) in supposition:
    #                 supposition[str(driver["driver"])] = []
    #
    #             supposition[str(driver["driver"])].append(best)
    #             ## TODO need to sort deliveries order once driver get them
    #             break


    return supposition




