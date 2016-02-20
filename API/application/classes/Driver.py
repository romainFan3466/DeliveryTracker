from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any
from application.classes.User import User

class Driver():

    # currentLocation = ""

    # def __init__(self, ID, name="", companyID=""):
    #     User.__init__(self, ID, name, companyID )

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
                Required("email") : User.email_validator(),
                Required("phone") : str
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)


    def update_parser(self):
        schema = {
            Required('driver'): {
                "name": All(str, Length(min=0)),
                "email": User.email_validator(),
                "phone": str
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)
