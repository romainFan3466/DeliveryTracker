from datetime import datetime
from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any
from flask import jsonify
class Delivery:

    # ID = ""
    # date_created = ""
    # date_pickup = ""
    # date_delivery = ""
    #
    # Location_delivery = ""
    # Location_pickup = ""
    #
    # customer_ID = ""
    # driver_ID = ""
    #
    #
    # def __init__(self,
    #              ID,
    #              customer_ID,
    #              date_created=None,
    #              date_pickup:datetime=None,
    #              date_delivery:datetime=None,
    #              driver_ID=None):
    #     self.ID = ID
    #     self.customer_ID = customer_ID
    #     self.date_created=date_created
    #     self.date_pickup=date_pickup
    #     self.date_delivery=date_delivery
    #     self.driver_ID=driver_ID

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

    def date_validator(self, format="%Y-%m-%d %H:%M:%S"):
        return lambda v: datetime.strptime(v, format)


    def weight_validator(self):
        def correct(weight):
            if (isinstance(weight, float) or isinstance(weight, int)) and weight < 36000 and weight > 0:
                return weight
            else:
                raise Invalid("value must be int or float between 0 and 36000")
        return correct


    def area_validator(self):
        def correct(area):
            if(isinstance(area, float) or isinstance(area, int)) and area < 50 and area > 0:
                return area
            else:
                raise Invalid("value must be int or float between 0 and 50")
        return correct


    def state_validator(self):
        def correct(state):
            supported_states = ["not taken", "taken", "picked up", "on way", "delivered", "canceled"]
            if state in supported_states:
                return state
            else:
                raise Invalid("Unsupported state")
        return correct


    def create_parser(self):
        schema  = {
            Required('delivery'): {
                Required("customer_id") : All(int, Range(min=0)),
                Required("date_created") : self.date_validator(),
                Required("date_due") : self.date_validator(),
                Required("weight") : self.weight_validator(),
                Required("area") : self.area_validator(),
                Required("content") : str,
                Required("sender_id"): All(int, Range(min=0)),
                Required("receiver_id"): All(int, Range(min=0)),
                "info" : str
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)



    def update_parser(self):
        schema  = {
            Required('delivery'): {
                "customer_id" : All(int, Range(min=0)),
                "date_pickup" : self.date_validator(),
                "date_delivery" : self.date_validator(),
                "date_due" : self.date_validator(),
                "weight" : self.weight_validator(),
                "area" : self.area_validator(),
                "content" : str,
                "sender_id" : All(int, Range(min=0)),
                "receiver_id" : All(int, Range(min=0)),
                "info" : str
            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)

    def getAll_parser(self):
        schema  = {
            'conditions': {
                "customer_id" : All(int, Range(min=0)),
                "start" : self.date_validator(),
                "end" : self.date_validator()

            }
        }
        return Schema(schema, extra=REMOVE_EXTRA)

    def update_state_parser(self):
        schema  = {
                Required("state") : self.state_validator(),
                Required("delivery_id") : All(int, Range(min=0))
        }

        return Schema(schema, extra=REMOVE_EXTRA)
