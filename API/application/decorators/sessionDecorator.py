from flask import session, abort
from functools import wraps

def required_user(user:str="admin"):
    def logged_in(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if user is logged
            if "user" in session and "id" in session["user"]:
                # if a admin is required
                if "type" in session["user"] and  session["user"]["type"]== user:
                    return f(*args, **kwargs)
            abort(401)
        return decorated_function
    return logged_in

