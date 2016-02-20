
from flask import url_for, session
import pytest_mock
#from unittest.mock import patch
import pytest
from application.core.DBHandler import DBHandler
from werkzeug.datastructures import FileStorage
from application.classes.Location import Location
import json
import datetime
import os


class TestBlueprintDelivery:


    delivery = {
        "delivery":{
            "sender_id": 5,
            "receiver_id" : 3,
            "customer_id" : 12,
            "date_created" : '2015-11-30 17:23:08',
            "date_due" : '2015-11-30 17:23:09',
            "weight": 356,
            "area" :2.4,
            "content": "fish"
        }
    }


############### CREATE #####################
    def test_create_not_authorized(self, client):
        wrong_delivery = {}
        res = client.post(url_for("delivery.create"), data=json.dumps(wrong_delivery), content_type='application/json')
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_create_missing_params(self, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }

        wrong_delivery = {}
        res = client.post(url_for("delivery.create"), data=json.dumps(wrong_delivery), content_type='application/json')
        assert res.status_code == 400


    def test_create_with_wrong_customer_receiver_sender_id(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }

        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.post(url_for("delivery.create"), data=json.dumps(self.delivery), content_type='application/json')
        assert res.status_code == 404
        assert res.json == {"info": "Customer not found"}
        mocker.stopall()

    def test_create_with_wrong_date_format(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        delivery = {
            "delivery": {
                "sender_id": 5,
                "receiver_id": 3,
                "customer_id": 12,
                "date_due": '2015-11-30 17:23:09',
                "weight": 356,
                "area": 2.4,
                "content": "fish",
                "date_created": '2015-11304653656DFG'
            }
        }

        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.post(url_for("delivery.create"), data=json.dumps(delivery), content_type='application/json')
        assert res.status_code == 400
        mocker.stopall()


    def test_create_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        mocker.patch.object(DBHandler, "insert", return_value=34)
        res = client.post(url_for("delivery.create"), data=json.dumps(self.delivery), content_type='application/json')
        assert res.status_code == 200
        assert res.json == {"info": "Delivery created successfully", "deliveryId": 34}
        mocker.stopall()



############### UPDATE #####################
    def test_update_unauthorized(self, client, mocker):
        res = client.put(url_for("delivery.update", id=12))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}
        mocker.stopall()


    def test_update_with_wrong_delivery_id(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.put(url_for("delivery.update", id=12))
        assert res.status_code == 404
        assert res.json == {"info" : "Delivery not found"}
        mocker.stopall()


    def test_update_with_wrong_params(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("delivery.update", id=12),  data=json.dumps({}), content_type='application/json')
        assert res.status_code == 400
        mocker.stopall()
    

    def test_update_with_wrong_customer_sender_receiver(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }

        def is_existing(table, **kwargs):
            return table == "deliveries"
        
        wrong_delivery = {
            "delivery":{
                "customer_id" : 2
            }
        }    
        mocker.patch.object(DBHandler, "is_existing", side_effect=is_existing)
        res = client.put(url_for("delivery.update", id=12),  data=json.dumps(wrong_delivery), content_type='application/json')
        assert res.status_code == 404
        assert res.json == {"info" : "Customer not found"}
        mocker.stopall()






    def test_update_wrong_date_format(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }

        _delivery = {
            "delivery":{
                 "sender_id": 5,
                "receiver_id": 3,
                "customer_id": 12,
                "date_created": '2015-11-30 17:23:09',
                "weight": 356,
                "area": 2.4,
                "content": "fish",
                "date_due" : "13/12/2015",
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("delivery.update", id=12),  data=json.dumps(_delivery), content_type='application/json')
        assert res.status_code == 400
        mocker.stopall()

    

    def test_update_with_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }


        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        mocker.patch.object(DBHandler, "update", return_value=True)
        res = client.put(url_for("delivery.update", id=12),  data=json.dumps(self.delivery), content_type='application/json')
        assert res.status_code == 200
        assert res.json == {"info" : "Delivery updated successfully"}
        mocker.stopall()



############### DELETE #####################

    def test_delete_with_unauthorized(self, client, mocker):
        res = client.delete(url_for("delivery.delete", id=12))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_delete_with_wrong_delivery_id(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.delete(url_for("delivery.delete", id=12))
        assert res.status_code == 404
        assert res.json == {"info" : "Delivery not found"}
        mocker.stopall()



    def test_delete_with_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        mocker.patch.object(DBHandler, "delete", return_value=True)
        res = client.delete(url_for("delivery.delete", id=12))
        assert res.status_code == 200
        assert res.json == {"info" : "Delivery deleted successfully"}
        mocker.stopall()


############ GET #######################

    def test_get_unauthorized(self, client, mocker):
        res = client.get(url_for("delivery.get", id=12))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_get_with_wrong_id(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "select", return_value=None)
        res = client.get(url_for("delivery.get", id=12))
        assert res.status_code == 404
        assert res.json == {"info" : "Delivery not found"}
        mocker.stopall()


    def test_get_with_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        delivery_sql = {
            "id" : 2,
            "customer_id" : 34,
            "driver_id" : 5,
            "date_pickup" : datetime.datetime.strptime('2015-11-30 17:23:09', "%Y-%m-%d %H:%M:%S"),
            "date_delivery" : datetime.datetime.strptime('2015-11-30 17:23:10', "%Y-%m-%d %H:%M:%S"),
            "date_created" : datetime.datetime.strptime('2015-10-30 19:23:10', "%Y-%m-%d %H:%M:%S"),
            "date_due" : datetime.datetime.strptime('2015-11-30 16:23:10', "%Y-%m-%d %H:%M:%S"),
            "weight": 12,
            "area": 10.1,
            "content": "fish",
            "sender_id": 2,
            "receiver_id": 3,
            "info": "",
            "canceled" : 0,
            "state" : "not taken"
        }

        expected_delivery = {
            "delivery":{
                "id" : 2,
                "customer_id" : 34,
                "driver_id" : 5,
                "date_pickup" : '2015-11-30 17:23:09',
                "date_delivery" : '2015-11-30 17:23:10',
                "date_created" : '2015-10-30 19:23:10',
                "date_due" : '2015-11-30 16:23:10',
                "weight": 12,
                "area": 10.1,
                "content": "fish",
                "sender_id": 2,
                "receiver_id": 3,
                "info": "",
                "canceled" : False,
                "state" : "not taken"
            }
        }
        mocker.patch.object(DBHandler, "select", return_value=delivery_sql)
        res = client.get(url_for("delivery.get", id=2))
        assert res.status_code == 200
        assert "delivery" in res.json
        assert res.json["delivery"] == expected_delivery["delivery"]
        mocker.stopall()

############## GET ALL ######################## TODO : uncompleted

    def test_get_all_unauthorized(self, client, mocker):
        res = client.post(url_for("delivery.getAll"))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_get_all_with_no_recorded_delivery(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        cond= {"conditions" : {}}
        mocker.patch.object(DBHandler, "query", return_value=[])
        res = client.post(url_for("delivery.getAll"),data=json.dumps(cond), content_type='application/json')
        assert res.status_code == 200
        assert "deliveries" in res.json
        assert isinstance(res.json["deliveries"], list)
        assert len(res.json["deliveries"]) == 0
        mocker.stopall()


    def test_get_all_with_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        delivery_sql = [{
            "id" : 2,
            "customer_id" : 34,
            "driver_id" : 5,
            "date_pickup" : datetime.datetime.strptime('2015-11-30 17:23:09', "%Y-%m-%d %H:%M:%S"),
            "date_delivery" : datetime.datetime.strptime('2015-11-30 17:23:10', "%Y-%m-%d %H:%M:%S"),
            "date_created" : datetime.datetime.strptime('2015-10-30 19:23:10', "%Y-%m-%d %H:%M:%S"),
            "date_due" : datetime.datetime.strptime('2015-11-30 16:23:10', "%Y-%m-%d %H:%M:%S"),
            "weight": 12,
            "area": 10.1,
            "content": "fish",
            "sender_id": 2,
            "receiver_id": 3,
            "info": "",
            "canceled" : 0,
            "state" : "not taken",
            "customer_name": "my_customer"
        }]

        expected_delivery = {
            "deliveries": [
                {
                    "delivery": {
                        "id": 2,
                        "customer_id": 34,
                        "driver_id": 5,
                        "date_pickup": '2015-11-30 17:23:09',
                        "date_delivery": '2015-11-30 17:23:10',
                        "date_created": '2015-10-30 19:23:10',
                        "date_due": '2015-11-30 16:23:10',
                        "weight": 12,
                        "area": 10.1,
                        "content": "fish",
                        "sender_id": 2,
                        "receiver_id": 3,
                        "info": "",
                        "canceled": False,
                        "state": "not taken",
                        "customer_name": "my_customer"
                    }
                }
            ]
        }
        cond= {"conditions" : {}}
        mocker.patch.object(DBHandler, "query", return_value=delivery_sql)
        res = client.post(url_for("delivery.getAll"),data=json.dumps(cond), content_type='application/json')
        assert res.status_code == 200
        assert "deliveries" in res.json
        assert isinstance(res.json["deliveries"], list)
        assert res.json["deliveries"] == expected_delivery["deliveries"]
        mocker.stopall()


############## ASSIGN ########################

    def test_assign_unauthorized(self, client, mocker):
        res = client.put(url_for("delivery.assign_Driver", delivery_id=12, driver_id=2))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_assign_with_wrong_driver_id(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        def is_existing(table, **kwargs):
            return table != "users"

        mocker.patch.object(DBHandler, "is_existing", side_effect=is_existing)
        res = client.put(url_for("delivery.assign_Driver", delivery_id=12, driver_id=2))
        assert res.status_code == 404
        assert res.json == {"info": "Driver not found"}
        mocker.stopall()


    def test_assign_with_wrong_delivery_id(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        def is_existing(table, **kwargs):
            return table != "deliveries"

        mocker.patch.object(DBHandler, "is_existing", side_effect=is_existing)
        res = client.put(url_for("delivery.assign_Driver", delivery_id=12, driver_id=2))
        assert res.status_code == 404
        assert res.json == {"info": "Delivery not found"}
        mocker.stopall()


    def test_assign_with_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        mocker.patch.object(DBHandler, "update", return_value=True)
        res = client.put(url_for("delivery.assign_Driver", delivery_id=12, driver_id=2))
        assert res.status_code == 200
        assert res.json == {"info": "Driver has been assigned"}
        mocker.stopall()


############## UPLOAD SIGNATURE ########################

    def test_update_signature_unauthorized(self, client, mocker, config):
        file_path = os.path.join(config['UPLOAD_FOLDER'], "17.png")
        files = {'file': open(file_path, 'rb')}
        res = client.post(url_for("delivery.upload_signature", delivery_id=12), data=files)
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_update_signature_admin_unauthorized(self, client, mocker, config):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        file_path = os.path.join(config['UPLOAD_FOLDER'], "17.png")
        files = {'file': open(file_path, 'rb')}
        res = client.post(url_for("delivery.upload_signature", delivery_id=12), data=files)
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_update_signature_wrong_delivery(self, client, mocker, config):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "driver",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.post(url_for("delivery.upload_signature", delivery_id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Delivery not found'}
        mocker.stopall()


    def test_update_signature_no_file(self, client, mocker, config):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "driver",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.post(url_for("delivery.upload_signature", delivery_id=12), data={})
        assert res.status_code == 400
        mocker.stopall()


    def test_update_signature_wrong_content(self, client, mocker, config):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "driver",
                "company_id": 2
            }
        files = {'file': FileStorage(filename="16.jpg", name="16.jpg",content_type="image/jpg")}
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        # mocker.patch.object(FileStorage, "save", return_value=True)
        res = client.post(url_for("delivery.upload_signature", delivery_id=12), data=files)
        assert res.status_code == 400
        assert res.json == {'info': "Content type must be 'image/png'"}
        mocker.stopall()


    def test_update_signature_success(self, client, mocker, config):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "driver",
                "company_id": 2
            }
        file_path = os.path.join(config['UPLOAD_FOLDER'], "17.png")
        files = {'file': open(file_path, 'rb')}
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        mocker.patch.object(FileStorage, "save", return_value=True)
        res = client.post(url_for("delivery.upload_signature", delivery_id=12), data=files)
        assert res.status_code == 200
        assert res.json == {'info': 'ok'}
        mocker.stopall()


############## GET SIGNATURE ########################

    def test_get_signature_unauthorized(self, client, mocker, config):
        res = client.get(url_for("delivery.get_signature", delivery_id=12))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_get_signature_wrong_delivery(self, client, mocker, config):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.get(url_for("delivery.get_signature", delivery_id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Delivery not found'}
        mocker.stopall()



    def test_get_signature_not_found(self, client, mocker, config):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        mocker.patch.object(os.path, "isfile", return_value=False)
        res = client.get(url_for("delivery.get_signature", delivery_id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Signature not found'}
        mocker.stopall()



    def test_get_signature_success(self, client, mocker, config):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.get(url_for("delivery.get_signature", delivery_id=17))
        assert res.status_code ==200
        assert res.content_type == "image/png"
        mocker.stopall()

############## UPDATE STATE ########################

