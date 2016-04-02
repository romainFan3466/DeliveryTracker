from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any
from application.core.validator import *
class Vehicle:


    def __init__(self, data=None):
        schema = {
            Required("registration") : str,
            Required("type") : str,
            Required("id") : All(int, Range(min=0)),
            Required("area") : area_validator(nullable=True),
            Required("weight") : weight_validator(nullable=True),
            Required("max_weight") : weight_validator(),
            Required("max_area") : area_validator()
        }
        parser = Schema(schema, extra=REMOVE_EXTRA)

        if data:
            obj = parser(data)
            for k,v in obj.items():
                setattr(self,k,v)


    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def get_id(self):
       return self.id if hasattr(self ,"id") else None


    def get_free_area(self):
        if hasattr(self, "area") and hasattr(self, "max_area"):
            free = self.max_area - self.area
            return free if free>0 else -1
        else:
            return None


    def get_free_weight(self):
        if hasattr(self, "weight") and hasattr(self, "max_weight"):
            free = self.max_weight - self.weight
            return free if free>0 else -1
        else:
            return None


    @staticmethod
    def parse(data: dict, method: str):
        internal_method = method + "_parser"
        try:
            parser = getattr(Vehicle(), internal_method)()
            return parser(data)
        except (NameError, AttributeError, MultipleInvalid) as e:
            if isinstance(e, MultipleInvalid):
                errors_name = [str(e) for e in e.errors]
                return {"errors": errors_name}
            return "Unsupported method"


    def create_parser(self):
        schema  = {
            Required('vehicle'): {
                Required("registration") : str,
                Required("type") : str,
                Required("max_weight") : All(Any(float, int), Range(min=0)),
                Required("max_area") : All(Any(float, int), Range(min=0)),
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)


    def update_parser(self):
        schema = {
            Required('vehicle'): {
                "registration" : str,
                "type" : str,
                "max_weight" : All(Any(float, int), Range(min=0)),
                "max_area" : All(Any(float, int), Range(min=0)),
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)
