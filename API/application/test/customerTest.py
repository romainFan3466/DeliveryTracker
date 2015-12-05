
from flask import url_for
import pytest
from application.core.DBHandler import DBHandler
from application.classes.Location import Location
import json

class TestBlueprintCustomer:

    customer = {
            "customer":{
                "name" : "romain",
                "location":{
                    "lat": 12.343545,
                    "lng": 2.345435,
                },
                "phone":"546456445"
            }
        }



###############CREATE ############################"


    def test_create_with_wrong_params(self, client):
        res = client.post(url_for('customer.create'), data=json.dumps({}),  content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}



    def test_create_with_existing_customer(self, client, mocker):
        def  is_existing(table, **kwargs):
            if table == "customers" :
                return True

        mocker.patch.object(DBHandler, 'is_existing',  side_effect=is_existing)
        res = client.post(url_for('customer.create'), data=json.dumps(self.customer), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Customer with the same name already exist'}
        mocker.stopall()



    def test_create_with_success_no_location_creation(self, client, mocker):
        def is_existing(table, **kwargs):
            if table == "customers" :
                return False
        mocker.patch.object(DBHandler, 'is_existing', side_effect=is_existing)
        mocker.patch.object(Location, 'getIdFromDB', return_value=3)
        mocker.patch.object(DBHandler, 'insert', return_value=12)
        res = client.post(url_for('customer.create'), data=json.dumps(self.customer), content_type='application/json')
        assert res.status_code == 200
        assert res.json == {"info":"Customer created successfully", "customerId":12}
        mocker.stopall()



    def test_create_with_success_and_location_creation(self, client, mocker):
        def  is_existing(table, **kwargs):
            if table == "customers" :
                return False

        def insert(table, **kwargs):
            return 12 if table == "customers" or table == "locations" else None

        mocker.patch.object(DBHandler, 'select', return_value=None)
        mocker.patch.object(DBHandler, 'is_existing',  side_effect=is_existing)
        mocker.patch.object(DBHandler, "insert", side_effect=insert)
        res = client.post(url_for('customer.create'), data=json.dumps(self.customer), content_type='application/json')
        assert res.status_code == 200
        assert res.json == {"info":"Customer created successfully", "customerId":12}
        mocker.stopall()


    ############## DELETE ######################

    def test_delete_with_wrong_params(self, client, mocker):
        mocker.patch.object(DBHandler, 'is_existing',  return_value=False)
        res = client.delete(url_for('customer.delete', id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Customer not found'}
        mocker.stopall()


    def test_delete_with_success(self, client, mocker):
        mocker.patch.object(DBHandler, 'is_existing',  return_value=True)
        mocker.patch.object(DBHandler, 'delete',  return_value=True)
        res = client.delete(url_for('customer.delete', id=12))
        assert res.status_code == 200
        assert res.json == {"info":"Customer deleted successfully"}
        mocker.stopall()


 ############## GET ######################

    def test_get_with_wrong_params(self, client, mocker):
        mocker.patch.object(DBHandler, 'query',  return_value=None)
        res = client.get(url_for('customer.get', id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Customer not found'}
        mocker.stopall()


    def test_get_with_success(self, client, mocker):
        sql_result = {
            "id" : 12,
            "name" : "romain",
            "location_lat": 12.343545,
            "location_lng": 2.345435,
            "phone":"546456445"
        }
        mocker.patch.object(DBHandler, 'query',  return_value=sql_result)
        res = client.get(url_for('customer.get', id=12))
        c = {
            "customer":{
                "id" : 12,
                "name" : "romain",
                "location":{
                    "lat": 12.343545,
                    "lng": 2.345435,
                },
                "phone":"546456445"
            }
        }
        assert res.status_code == 200
        assert res.json == c
        mocker.stopall()


 ############## UPDATE ######################

    def test_update_with_wrong_customer_id(self, client, mocker):
        mocker.patch.object(DBHandler, 'is_existing', return_value=False)
        res = client.put(url_for('customer.update', id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Customer not found'}
        mocker.stopall()


    def test_update_with_wrong_params(self, client, mocker):
        mocker.patch.object(DBHandler, 'is_existing', return_value=True)
        res = client.put(url_for('customer.update', id=12), data=json.dumps({}),  content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()


    def test_update_with_existing_customer_name(self, client, mocker):
        customer_req = {
            "customer" : {
                "name" : "romain"
            }
        }
        mocker.patch.object(DBHandler, 'is_existing', return_value=True)
        res = client.put(url_for('customer.update', id=12), data=json.dumps(customer_req), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Customer with the same name already exists'}
        mocker.stopall()


    def test_update_with_success(self, client, mocker):
        def is_existing(table, conditions, **kwargs):
            if table == "customers":
                if "id" in conditions:
                    return True
                if "name" in conditions:
                    return False

        customer_req = {
            "customer" : {
                "name" : "romain",
                "location" : {
                    "lat": 23.456,
                    "lng": 4.4654
                },
                "phone": "325345345"
            }
        }
        mocker.patch.object(DBHandler, 'is_existing', side_effect=is_existing)
        mocker.patch.object(Location, 'getIdFromDB', return_value=34)
        mocker.patch.object(DBHandler, 'update', return_value=True)
        res = client.put(url_for('customer.update', id=12), data=json.dumps(customer_req), content_type='application/json')
        assert res.status_code == 200
        assert res.json == {"info": "Customer data updated successfully"}
        mocker.stopall()



############## GET ALL ###############
    def test_getAll_with_no_customers(self, client, mocker):
        mocker.patch.object(DBHandler, "query", return_value=[])
        res = client.get(url_for("customer.getAll"))
        assert "customers" in res.json
        assert isinstance(res.json["customers"], list)
        assert len(res.json["customers"]) == 0
        assert res.status_code == 200


    def test_getAll_with_customers(self, client, mocker):
        sql_result = [{
            "id" : 12,
            "name" : "romain",
            "location_lat": 12.343545,
            "location_lng": 2.345435,
            "phone":"546456445"
        }]

        _customer = {
            "customer":{
                "id" : 12,
                "name" : "romain",
                "location":{
                    "lat": 12.343545,
                    "lng": 2.345435,
                },
                "phone":"546456445"
            }
        }


        mocker.patch.object(DBHandler, "query", return_value=sql_result)
        res = client.get(url_for("customer.getAll"))
        assert "customers" in res.json
        assert isinstance(res.json["customers"], list)
        assert len(res.json["customers"]) == 1
        assert res.json["customers"][0] == _customer
        assert res.status_code == 200

