from application.classes import User

class Administrator(User):


    def __init__(self, ID, name="", companyID=""):
        self.ID = ID
        self.name = name
        self.company_ID = companyID


