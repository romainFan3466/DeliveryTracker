from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any
from application.core.validator import email_validator

class User:

    @staticmethod
    def parse(data:dict, method:str):
        internal_method =method + "_parser"
        try:
            parser = getattr(User(), internal_method)()
            return parser(data)
        except (NameError, AttributeError, MultipleInvalid) as e :
            if isinstance(e, MultipleInvalid):
                errors_name = [str(e) for e in e.errors]
                return {"errors" : errors_name}
            return "Unsupported method"



    @staticmethod
    def type_validator():
        def correct(type):
            if isinstance(type, str) and type in ["admin", "driver"]:
                return type
            raise Invalid("value must be 'admin' or 'driver'")
        return correct


    def create_parser(self):
        schema  = {
            Required('user'): {
                Required("email") : email_validator,
                Required("password") : str,
                Required("type") : self.type_validator()
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)

