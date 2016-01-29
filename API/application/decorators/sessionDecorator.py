from flask import session, abort
from functools import wraps

def required_user(user:str=""):
    def logged_in(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if user is logged
            v = session
            if "user" in session and "id" in session["user"]:
                if user == "":
                    return f(*args, **kwargs)
                # if a specific type is required
                elif "type" in session["user"] and  session["user"]["type"]== user:
                    return f(*args, **kwargs)
            abort(401)
        return decorated_function
    return logged_in

