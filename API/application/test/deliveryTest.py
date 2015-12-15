
from flask import url_for, session
import pytest_mock
#from unittest.mock import patch
import pytest
from application.core.DBHandler import DBHandler
from application.classes.Location import Location
import json
import datetime


class TestBlueprintDelivery:


    delivery = {
        "delivery":{
            "location_delivery": {
                "lat" : 12.4354645,
                "lng" : 34.3453453
            },
            "location_pickup" : {
                "lat" : 17.435645,
                "lng" : 35.3453453
            },
            "customer_id" : 12,
            "date_created" : '2015-11-30 17:23:08',
            "date_pickup" : '2015-11-30 17:23:09',
            "date_delivery" : '2015-11-30 17:23:10'
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
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}


    def test_create_with_wrong_customer_id(self, client, mocker):
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
                "location_delivery": {
                    "lat": 12.4354645,
                    "lng": 34.3453453
                },
                "location_pickup": {
                    "lat": 17.435645,
                    "lng": 35.3453453
                },
                "customer_id": 12,
                "date_created": '2015-11304653656DFG',
            }
        }

        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.post(url_for("delivery.create"), data=json.dumps(delivery), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
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
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()
    

    def test_update_with_wrong_customer(self, client, mocker):
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



    def test_update_with_wrong_pickup(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        wrong_delivery = {
            "delivery": {
                "location_pickup" : {
                    "lat" : -170.435645,
                    "lng" : 354.3453453
                }
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("delivery.update", id=12), data=json.dumps(wrong_delivery),content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()


    def test_update_with_wrong_delivery(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        wrong_delivery = {
            "delivery": {
                "location_delivery" : {
                    "lat" : -170.435645,
                    "lng" : 354.3453453
                }
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("delivery.update", id=12), data=json.dumps(wrong_delivery),content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
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
                "date_pickup" : "13/12/2015",
                "date_delivery" : "13/01/2016"
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("delivery.update", id=12),  data=json.dumps(_delivery), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()

    

    def test_update_with_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }

        _delivery = {
            "delivery":{
                "customer_id" : 2,
                "location_delivery" : {
                    "lat": 23.4555,
                    "lng": 45.5677
                },
                "location_pickup" : {
                    "lat": 22.4555,
                    "lng": 4.5677
                },
                "date_pickup" : '2015-11-30 17:23:09',
                "date_delivery" : '2015-11-30 17:23:10'
            }
        }

        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        mocker.patch.object(DBHandler, "update", return_value=True)
        res = client.put(url_for("delivery.update", id=12),  data=json.dumps(_delivery), content_type='application/json')
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
            "date_pickup" : '2015-11-30 17:23:09',
            "date_delivery" : '2015-11-30 17:23:10',
            "date_created" : '2015-10-30 19:23:10',
            "location_pickup_lat" : 12.45654,
            "location_pickup_lng" : 2.46654,
            "location_delivery_lat" : 24.45654,
            "location_delivery_lng" : 3.46654
        }

        expected_delivery = {
            "id" : 2,
            "customer_id" : 34,
            "driver_id" : 5,
            "date_pickup" : '2015-11-30 17:23:09',
            "date_delivery" : '2015-11-30 17:23:10',
            "date_created" : '2015-10-30 19:23:10',
             "location_pickup" : {
                    "lat" : 12.45654,
                    "lng" : 2.46654,
                },
                "location_delivery" : {
                    "lat" : 24.45654,
                    "lng" : 3.46654
                }
        }
        mocker.patch.object(DBHandler, "select", return_value=delivery_sql)
        res = client.get(url_for("delivery.get", id=2))
        assert res.status_code == 200
        assert "delivery" in res.json
        assert res.json["delivery"] == expected_delivery

############## GET ALL ########################

    def test_get_all_unauthorized(self, client, mocker):
        res = client.get(url_for("delivery.getAll"))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_get_all_with_no_recorded_delivery(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "select", return_value=[])
        res = client.get(url_for("delivery.getAll"))
        assert res.status_code == 200
        assert "deliveries" in res.json
        assert isinstance(res.json["deliveries"], list)
        assert len(res.json["deliveries"]) == 0



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
            "date_pickup" : '2015-11-30 17:23:09',
            "date_delivery" : '2015-11-30 17:23:10',
            "date_created" : '2015-10-30 19:23:10',
            "location_pickup_lat" : 12.45654,
            "location_pickup_lng" : 2.46654,
            "location_delivery_lat" : 24.45654,
            "location_delivery_lng" : 3.46654
        }]

        expected_delivery = {
            "delivery" : {
                "id" : 2,
                "customer_id" : 34,
                "driver_id" : 5,
                "date_pickup" : '2015-11-30 17:23:09',
                "date_delivery" : '2015-11-30 17:23:10',
                "date_created" : '2015-10-30 19:23:10',
                 "location_pickup" : {
                        "lat" : 12.45654,
                        "lng" : 2.46654,
                    },
                    "location_delivery" : {
                        "lat" : 24.45654,
                        "lng" : 3.46654
                    }

                }
        }
        mocker.patch.object(DBHandler, "select", return_value=delivery_sql)
        res = client.get(url_for("delivery.getAll"))
        assert res.status_code == 200
        assert "deliveries" in res.json
        assert isinstance(res.json["deliveries"], list)
        assert res.json["deliveries"][0] == expected_delivery

