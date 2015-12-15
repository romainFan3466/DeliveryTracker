from flask import jsonify, request
from functools import wraps
from application.classes.Location import Location
def checkLocation():
    def check(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            res = request.get_json(force=True)
            if "location" in res and "lat"in res["location"] and "lng" in res["location"]:
                lat = res["location"]["lat"]
                lng = res["location"]["lng"]

                if Location.isValid(lat,lng):
                    return f(lat=lat, lng=lng)
                return jsonify(info="Location coordinates not acceptable; Latitude (S-N): -90 to +90; Longitude (W-E): -180 to +180"),400
        return decorated_function
    return check
