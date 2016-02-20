from application.classes.Location import Location
from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any


class Customer:
    # ID = ""
    # name = ""
    # location = ""
    # phone = ""
    # 
    # 
    # def __init__(self, ID, name="", location="", phone="" ):
    # 
    #     self.ID=ID
    # 
    #     self.name=name
    #     #self.location=Location(location)
    #     self.phone=phone



    @staticmethod
    def parse(data: dict, method: str):
        internal_method = method + "_parser"
        try:
            parser = getattr(Customer(), internal_method)()
            return parser(data)
        except (NameError, AttributeError, MultipleInvalid) as e :
            if isinstance(e, MultipleInvalid):
                errors_name = [str(e) for e in e.errors]
                return {"errors" : errors_name}
            return "Unsupported method"


    def create_parser(self):
        schema = {
            Required('customer'): {
                Required("name"): str,
                Required("address"): str,
                Required("location"): {
                    Required("lat") : All(float, Range(min=-90.0, max=90.0)),
                    Required("lng") : All(float, Range(min=-180.0, max=180.0))
                },
                Required("phone"): str,
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)


    def update_parser(self):
        schema = {
            Required('customer'): {
                "name" : str,
                "address" : str,
                "location" : {
                    Required("lat") : All(float, Range(min=-90.0, max=90.0)),
                    Required("lng") : All(float, Range(min=-180.0, max=180.0))
                },
                "phone": str,
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)
