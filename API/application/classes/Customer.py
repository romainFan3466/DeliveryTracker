
from application.classes import Location, Delivery
class Customer:

    ID = ""
    name = ""
    location = ""
    phone = ""


    def __init__(self, ID, name="", location="", phone="" ):

        self.ID=ID

        self.name=name
        #self.location=Location(location)
        self.phone=phone






