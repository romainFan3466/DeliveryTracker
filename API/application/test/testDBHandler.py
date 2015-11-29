
from application.core.DBHandler import DBHandler

config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "jf/b6rb",
            "database": "deliveryTracker",
    }

db = DBHandler(config)

email = "romain.fanara@sfr.fr"
_SQL = ("SELECT password AS salted_password, type FROM users WHERE email = %s ;")


# query = db.query(_SQL, (email,))

# res = db.is_existing(table="customers", conditions={"id": 2})

# res = db.select(table="customers", selected_columns=("id", "name","locationId"), conditions={"id":3}, multiple=False)

res = db.delete("customers",{'id':3})

#res= db.select("customers",("*"),{"id":3})


print(res)
