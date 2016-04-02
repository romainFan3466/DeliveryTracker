from datetime import datetime
from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any
from application.core.validator import *
class Delivery:


    def __init__(self, data=None):
        schema = {
            Required("id"): All(int, Range(min=0)),
            Required("customer_id"): All(int, Range(min=0)),
            Required("sender_id"): All(int, Range(min=0)),
            Required("receiver_id"): All(int, Range(min=0)),
            Required("date_created"): date_validator,
            Required("date_due"): date_validator,
            Required("date_pickup"): date_validator,
            Required("date_delivery"): date_validator,
            Required("weight"): weight_validator(),
            Required("area"): area_validator(),
            Required("content"): str,
            Required("canceled"): All(int, Range(min=0, max=1)),
            Required("state") : self.state_validator,
            Required("driver_id"): id_validator,
            "customer_name" : str,
            "num_order" : All(int, Range(min=1)),
            "info": Any(str, None),
            "sender_lat" : All(Any(float, Decimal), Range(min=-90.0, max=90.0)),
            "sender_lng" : All(Any(float, Decimal), Range(min=-180.0, max=180.0)),
            "receiver_lat" : All(Any(float, Decimal), Range(min=-90.0, max=90.0)),
            "receiver_lng" : All(Any(float, Decimal), Range(min=-180.0, max=180.0))
        }
        parser = Schema(schema, extra=REMOVE_EXTRA)

        if data:
            obj = parser(data)
            for k,v in obj.items():
                if k == "canceled":
                    setattr(self,k, v!=0)
                else:
                    setattr(self,k,v)


    def __eq__(self, other):
        return self.__dict__ == other.__dict__



    def to_dict(self):
        d = self.__dict__.copy()
        d["date_pickup"] = self.date_pickup.strftime("%Y-%m-%d %H:%M:%S") if hasattr(self,"date_pickup") and self.date_pickup is not None else None
        d["date_delivery"] = self.date_delivery.strftime("%Y-%m-%d %H:%M:%S") if hasattr(self,"date_delivery") and self.date_delivery is not None  else None
        d["date_due"] = self.date_due.strftime("%Y-%m-%d %H:%M:%S") if hasattr(self,"date_due") and self.date_due is not None else None
        d["date_created"] = self.date_created.strftime("%Y-%m-%d %H:%M:%S") if hasattr(self,"date_created") and self.date_created is not None else None
        return d


    def getReceiverLocation(self):
        return {"lat" : float(self.receiver_lat), "lng": float(self.receiver_lng)}


    def getSenderLocation(self):
        return {"lat" : float(self.sender_lat), "lng": float(self.sender_lng)}


    def get_area(self):
        return self.area if hasattr(self, "area") else None


    def get_weight(self):
        return self.weight if hasattr(self, "weight") else None


    @staticmethod
    def parse(data:dict, method:str):
        internal_method =method + "_parser"
        try:
            parser = getattr(Delivery(), internal_method)()
            return parser(data)
        except (NameError, AttributeError, MultipleInvalid) as e :
            if isinstance(e, MultipleInvalid):
                errors_name = [str(e) for e in e.errors]
                return {"errors" : errors_name}
            return "Unsupported method"


    def state_validator(self, state):
        supported_states = ["not taken", "taken", "picked up", "on way", "delivered", "not assigned", "canceled"]
        if state in supported_states:
            return state
        else:
            raise Invalid("Unsupported state")


    def create_parser(self):
        schema  = {
            Required('delivery'): {
                Required("customer_id") : All(int, Range(min=0)),
                Required("date_created") : date_validator,
                Required("date_due") : date_validator,
                Required("weight") : weight_validator(),
                Required("area") : area_validator(),
                Required("content") : str,
                Required("sender_id"): All(int, Range(min=0)),
                Required("receiver_id"): All(int, Range(min=0)),
                "info": Any(str, None)
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)


    def update_parser(self):
        schema  = {
            Required('delivery'): {
                "customer_id" : All(int, Range(min=0)),
                "date_pickup" : date_validator,
                "date_delivery" : date_validator,
                "date_due" : date_validator,
                "weight" : weight_validator(),
                "area" : area_validator(),
                "content" : str,
                "sender_id" : All(int, Range(min=0)),
                "receiver_id" : All(int, Range(min=0)),
                "info": Any(str, None)
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)


    def getAll_parser(self):
        schema  = {
            'conditions': {
                "customer_id" : All(int, Range(min=0)),
                "start" : date_validator,
                "end" : date_validator,
                "state" : self.state_validator
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)


    def get_all_unassigned_parser(self):
        schema = {
            "customer_id": All(int, Range(min=0)),
            "start": date_validator,
            "end": date_validator,
            "state" : self.state_validator
        }

        return Schema(schema, extra=REMOVE_EXTRA)


    def update_state_parser(self):
        schema  = {
                Required("state") : self.state_validator,
                Required("delivery_id") : All(int, Range(min=0))
        }

        return Schema(schema, extra=REMOVE_EXTRA)


