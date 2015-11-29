__author__ = 'romain'
from flask import url_for
import pytest_mock
#from unittest.mock import patch
import pytest
from application.core.DBHandler import DBHandler
import json

class TestBlueprintCustomer:
    """
        - Mock a method from class :
            mocker.patch.object(DBHandler, 'select', return_value=customer,  side_effect=mymethod)

        - stop mocker
            mocker.stopall()


        - url_for use :
            url_for('customer.get', id=12)
            client.post("url", data=dict)

    """

    customer = {
            "customer":{
                "name" : "romain",
                "location":{
                    "lat": 12.343545,
                    "long": 2.345435,
                },
                "phone":"546456445"
            }
        }



###############CREATE ############################"


    def test_create_with_wrong_params(self, client, mocker):
        res = client.post(url_for('customer.create'), data={})
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



    def test_create_with_success(self, client, mocker):

        def  is_existing(table, **kwargs):
            if table == "customers" :
                return False

        def insert(table, **kwargs):
            return 12 if table == "customers" or table == "locations" else None

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


    def test_delete_with_no_sql_insert(self, client, mocker):
        mocker.patch.object(DBHandler, 'is_existing',  return_value=True)
        mocker.patch.object(DBHandler, 'delete',  return_value=False)
        res = client.delete(url_for('customer.delete', id=12))
        assert res.status_code == 500


    def test_delete_with_success(self, client, mocker):
        mocker.patch.object(DBHandler, 'is_existing',  return_value=True)
        mocker.patch.object(DBHandler, 'delete',  return_value=True)
        res = client.delete(url_for('customer.delete', id=12))
        assert res.status_code == 200
        assert res.json == {"info":"Customer deleted successfully"}


 ############## GET ######################

    def test_get_with_wrong_params(self, client, mocker):
        mocker.patch.object(DBHandler, 'select',  return_value=None)
        res = client.get(url_for('customer.get', id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Customer not found'}


    def test_get_with_success(self, client, mocker):
        mocker.patch.object(DBHandler, 'select',  return_value=self.customer["customer"])
        res = client.get(url_for('customer.get', id=12))
        assert res.status_code == 200
        assert res.json == self.customer
