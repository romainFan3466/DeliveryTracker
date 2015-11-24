from datetime import datetime

class Delivery:

    ID = ""
    date_created = ""
    date_pickup = ""
    date_delivery = ""

    Location_delivery = ""
    Location_pickup = ""

    customer_ID = ""
    driver_ID = ""


    def __init__(self,
                 ID,
                 customer_ID,
                 date_created=None,
                 date_pickup:datetime=None,
                 date_delivery:datetime=None,
                 driver_ID=None):
        self.ID = ID
        self.customer_ID = customer_ID
        self.date_created=date_created
        self.date_pickup=date_pickup
        self.date_delivery=date_delivery
        self.driver_ID=driver_ID




    