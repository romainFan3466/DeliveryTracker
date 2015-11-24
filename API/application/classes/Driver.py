from application.classes import User


class Driver(User):

    currentLocation = ""

    def __init__(self, ID, name="", companyID=""):
        User.__init__(self, ID, name, companyID )

