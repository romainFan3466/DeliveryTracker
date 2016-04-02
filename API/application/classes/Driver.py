from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any, Coerce
from application.core.validator import *
from decimal import *
import re
from application.classes.Vehicle import Vehicle
class Driver():

    # currentLocation = ""

    def     __init__(self, data=None):
        schema  = {
            Required("id") : All(int, Range(min=0)),
            Required("name") : All(str, Length(min=3)),
            "email" : email_validator,
            "phone" : str,
            Required("location_lat"): All(Any(float, Decimal), Range(min=-90.0, max=90.0)),
            Required("location_lng"): All(Any(float, Decimal), Range(min=-180.0, max=180.0)),
            "vehicle_id_1" : id_validator,
            "vehicle_id_2": id_validator,
            "v1_area": area_validator(nullable=True),
            "v1_max_area": area_validator(),
            "v1_weight" : weight_validator(nullable=True),
            "v1_max_weight" : weight_validator(),
            "v2_area": area_validator(nullable=True, none_allowed=True),
            "v2_max_area": area_validator(none_allowed=True),
            "v2_weight" : weight_validator(nullable=True, none_allowed=True),
            "v2_max_weight" : weight_validator(none_allowed=True)

        }
        parser = Schema(schema, extra=REMOVE_EXTRA)
        if data:
            obj = parser(data)
            for k,v in obj.items():
                if k == "location_lat" or k == "location_lng":
                    if not hasattr(self, "location"):
                        self.location = {}
                    self.location[k[-3:]] = v
                elif re.match(r'vehicle_id_[12]', k) :
                    if v is not None and "v" + k[-1] +"_area" in obj:
                        ve = {
                            "id" : obj["vehicle_id_"+k[-1]],
                            "registration" : "",
                            "type" : "",
                            "area" : obj["v"+k[-1]+"_area"],
                            "weight" : obj["v"+k[-1]+"_weight"],
                            "max_area" : obj["v"+k[-1]+"_max_area"],
                            "max_weight" : obj["v"+k[-1]+"_max_weight"],
                        }
                        setattr(self, "v"+k[-1], Vehicle(ve))
                    else:
                        setattr(self,k,v)
                else:
                    setattr(self,k,v) if not k[0]=="v" else None

    def to_dict(self):

        d= {
            "id" : self.id,
            "name":self.name,
        }
        if hasattr(self, "email"):
            d["email"] = self.email
        if hasattr(self, "email"):
            d["phone"] = self.phone
        if hasattr(self, "v1"):
            d["vehicle_id_1"] = self.v1.get_id()
        if hasattr(self, "v2"):
            d["vehicle_id_2"] = self.v2.get_id()

        return d

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def __str__(self):
        return str(self.id) if hasattr(self, "id") else "no id"

    def get_id(self):
        return self.id if hasattr(self ,"id") else None

    def getLocation(self):
        return {"lat": float(self.location["lat"]), "lng" : float(self.location["lng"])}


    def get_vehicles(self):
        result  = []
        if hasattr(self, "v1"):
            result.append(self.v1)
        if hasattr(self, "v2"):
            result.append(self.v2)
        return result

    def update_location(self, lat, lng):
        self.location = {"lat":lat, "lng":lng}


    def weight_validator(self):
        def correct(weight):
            if (isinstance(weight, float) or isinstance(weight, int) or isinstance(weight, Decimal)) and weight < 36000 and weight > 0:
                return float(weight)
            else:
                raise Invalid("value must be int or float between 0 and 36000")
        return correct


    def area_validator(self):
        def correct(area):
            if(isinstance(area, float) or isinstance(area, int) or isinstance(area, Decimal)) and area < 50 and area > 0:
                return float(area)
            else:
                raise Invalid("value must be int or float between 0 and 50")
        return correct

    @staticmethod
    def parse(data:dict, method:str):
        internal_method =method + "_parser"
        try:
            parser = getattr(Driver(), internal_method)()
            return parser(data)
        except (NameError, AttributeError, MultipleInvalid) as e :
            if isinstance(e, MultipleInvalid):
                errors_name = [str(e) for e in e.errors]
                return {"errors" : errors_name}
            return "Unsupported method"




    def create_parser(self):
        schema  = {
            Required('driver'): {
                Required("name") : All(str, Length(min=3)),
                Required("email") : email_validator,
                Required("phone") : str
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)


    def set_vehicle_parser(self):
        schema  = {
            Required('vehicles'): {
                Required("v1") : id_validator,
                Required("v2") : id_validator
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)


    def update_parser(self):
        schema = {
            Required('driver'): {
                "name": All(str, Length(min=0)),
                "email": email_validator,
                "phone": str
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)

