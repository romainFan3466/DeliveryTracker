from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any
import re

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
    def email_validator():
        def correct(email):
            if isinstance(email, str) and len(email) > 7:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                    return email
            raise Invalid("value must be an email address")
        return correct


    @staticmethod
    def type_validator():
        def correct(type):
            if isinstance(type, str) and type in ["admin", "driver"]:
                return type
            raise Invalid("value must be 'admin' or 'driver'")


    def create_parser(self):
        schema  = {
            Required('user'): {
                Required("email") : self.email_validator(),
                Required("password") : str,
                Required("type") : self.type_validator()
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)

