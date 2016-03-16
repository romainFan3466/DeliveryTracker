from datetime import datetime
from voluptuous import Invalid
from decimal import Decimal
import re


def date_validator(date, format="%Y-%m-%d %H:%M:%S"):
    if isinstance(date, str):
        return datetime.strptime(date, format)
    elif isinstance(date, datetime) or date is None:
        return date
    else:
        raise Invalid("value must be str, or datetime or None")


def id_validator(id):
    if (isinstance(id, int) and id>=0) or id is None:
        return id
    else:
        raise Invalid("value must be int > 0 or None")


def weight_validator(nullable=False, none_allowed=False):
    def correct(weight):
        if (isinstance(weight, float) or isinstance(weight, int) or isinstance(weight, Decimal)) and weight < 36000 and ((not nullable and weight > 0) or (nullable and weight>=0)):
            return float(weight)
        elif none_allowed is True and weight is None:
            return None
        else:
            raise Invalid("value must be int or float between 0 and 36000")
    return correct


def area_validator(nullable=False, none_allowed=False):
    def correct(area):
        if(isinstance(area, float) or isinstance(area, int) or isinstance(area, Decimal)) and area < 50 and ((not nullable and area > 0) or (nullable and area>=0)):
            return float(area)
        elif none_allowed is True and area is None:
            return None
        else:
            raise Invalid("value must be int or float between 0 and 50")
    return correct

def email_validator(email):
    if isinstance(email, str) and len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return email
    raise Invalid("value must be an email address")
