#!/usr/bin/python3

import requests
import json

s = requests.Session()


r = s.get("http://127.0.0.1:5000/api/status")

print(r.json())

data = {
    "user":{
        "email" : "romain.fanara@gmail.com",
        "password" : "1234"
    }
}


r = s.post("http://127.0.0.1:5000/api/signIn", data=json.dumps(data))
print(r.json())


r = s.get("http://127.0.0.1:5000/api/status")

print(r.json())
