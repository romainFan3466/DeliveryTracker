from voluptuous import Required, All, Length, Range, Schema, Invalid, MultipleInvalid, ALLOW_EXTRA, REMOVE_EXTRA, Object, Any

class Vehicle:

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
