from flask import jsonify
from functools import wraps

def checkLocation():
    def check(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
             if "lat" in kwargs and "lng" in kwargs :
                lat = kwargs["lat"]
                lng = kwargs["lng"]
                isCorrect = lat is int and lng is int and lat>=-90 and lat<=90 and lng>=-180 and lng<=180
                if isCorrect:
                    return f(*args, **kwargs)
                return jsonify(info="Location coordinates not accedable; Latitude (S-N): -90 to +90; Longitude (W-E): -180 to +180"),400
        return decorated_function
    return check
