from flask import url_for
import pytest_mock
#from unittest.mock import patch
import pytest
from application.core.DBHandler import DBHandler
from application.classes.Location import Location
import json
import datetime


class TestBlueprintDriver:

    driver = {
        "driver" : {
            "name" : "Romain",
            "email" : "romain@test.ie",
            "phone" : "5464654645"
        }
    }


##############" CREATE ######################"
    def test_create_unauthorized(self, mocker, client):
        wrong_delivery = {}
        res = client.post(url_for("driver.create"), data=json.dumps(wrong_delivery), content_type='application/json')
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_create_wrong_params(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        wrong_delivery = {}
        res = client.post(url_for("driver.create"), data=json.dumps(wrong_delivery), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}


    def test_create_existing_name(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.post(url_for("driver.create"), data=json.dumps(self.driver), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Driver with the same name already exist'}
        mocker.stopall()


    def test_create_existing_email(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }

        def is_existing(conditions, **kwargs):
            return "email" in conditions

        mocker.patch.object(DBHandler, "is_existing", side_effect=is_existing)
        res = client.post(url_for("driver.create"), data=json.dumps(self.driver), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Driver with the same email already exist'}
        mocker.stopall()


    def test_create_existing_success(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }

        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        mocker.patch.object(DBHandler, "insert", return_value=6)
        res = client.post(url_for("driver.create"), data=json.dumps(self.driver), content_type='application/json')
        assert res.status_code == 200
        assert "info" in res.json
        assert "driverId" in res.json
        assert "password" in res.json
        assert res.json["info"] == "Driver created successfully"
        assert res.json["driverId"] == 6
        mocker.stopall()

##############" UPDATE ######################"
    def test_update_unauthorized(self, mocker, client):
        wrong_delivery = {}
        res = client.put(url_for("driver.update", id=6), data=json.dumps(wrong_delivery), content_type='application/json')
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_update_wrong_driver(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        wrong_delivery = {}
        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.put(url_for("driver.update", id=12), data=json.dumps(wrong_delivery), content_type='application/json')
        assert res.status_code == 404
        assert res.json == {'info': "Driver not found"}
        mocker.stopall()


    def test_update_wrong_params(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        wrong_delivery = {}
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("driver.update", id=12), data=json.dumps(wrong_delivery), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()


    def test_update_wrong_name(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        def is_existing(conditions, **kwargs):
            return "name" in conditions or "id" in conditions

        mocker.patch.object(DBHandler, "is_existing", side_effect=is_existing)
        res = client.put(url_for("driver.update", id=12), data=json.dumps(self.driver), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': "Driver with the same name already exist"}
        mocker.stopall()


    def test_update_wrong_email(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        def is_existing(conditions, **kwargs):
            return "email" in conditions or "id" in conditions

        mocker.patch.object(DBHandler, "is_existing", side_effect=is_existing)
        res = client.put(url_for("driver.update", id=12), data=json.dumps(self.driver), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': "Driver with the same email already exist"}
        mocker.stopall()


    def test_update_success(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        def is_existing(conditions, **kwargs):
            return "id" in conditions

        mocker.patch.object(DBHandler, "is_existing", side_effect=is_existing)
        mocker.patch.object(DBHandler, "update", return_value=True)
        res = client.put(url_for("driver.update", id=12), data=json.dumps(self.driver), content_type='application/json')
        assert res.status_code == 200
        assert res.json == {'info': "Driver updated successfully"}
        mocker.stopall()