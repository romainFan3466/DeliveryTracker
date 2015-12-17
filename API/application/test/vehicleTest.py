from flask import url_for
import pytest_mock
#from unittest.mock import patch
import pytest
from application.core.DBHandler import DBHandler
from application.classes.Location import Location
import json
import datetime


class TestBlueprintVehicle:
    vehicle = {
        "vehicle" : {
            "registration" : "GHFDH546",
            "type" : "tractor",
            "max_weight" : 40.3,
            "max_area" : 34.45
        }
    }

    ##############" CREATE ######################"
    def test_create_unauthorized(self, mocker, client):
        res = client.post(url_for("vehicle.create"), data=json.dumps({}), content_type='application/json')
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_create_wrong_params(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        res = client.post(url_for("vehicle.create"), data=json.dumps({}), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}



    def test_create_existing_registration(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.post(url_for("vehicle.create"), data=json.dumps(self.vehicle) , content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Vehicle with the same registration already exist'}
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
        res = client.post(url_for("vehicle.create"), data=json.dumps(self.vehicle), content_type='application/json')
        assert res.status_code == 200
        assert "info" in res.json
        assert "vehicleId" in res.json
        assert res.json["info"] == "Vehicle created successfully"
        assert res.json["vehicleId"] == 6
        mocker.stopall()


    ##############" UPDATE ######################"
    def test_update_unauthorized(self, mocker, client):
        res = client.put(url_for("vehicle.update", id=6), data=json.dumps({}), content_type='application/json')
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_update_wrong_vehicle(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps({}), content_type='application/json')
        assert res.status_code == 404
        assert res.json == {'info': "Vehicle not found"}
        mocker.stopall()


    def test_update_wrong_params(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps({}), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()


    def test_update_existing_registration(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        _vehicle = {
            "vehicle" : {
                "registration" : "456GFH657"
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps(_vehicle), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Vehicle with the same registration already exist'}
        mocker.stopall()


    def test_update_wrong_max_weight(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        _vehicle = {
            "vehicle" : {
                "max_weight" : "dfgfg"
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps(_vehicle), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()
        
        
    def test_update_wrong_max_weight_overflow(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        _vehicle = {
            "vehicle" : {
                "max_weight" : 3000000
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps(_vehicle), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()
        
        
    def test_update_wrong_max_weight_overflow_negative(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        _vehicle = {
            "vehicle" : {
                "max_weight" : -30.35
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps(_vehicle), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()
        
    
    def test_update_wrong_max_area(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        _vehicle = {
            "vehicle" : {
                "max_area" : "dfgfg"
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps(_vehicle), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()
        
        
    def test_update_wrong_max_area_overflow(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        _vehicle = {
            "vehicle" : {
                "max_area" : 3000000
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps(_vehicle), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()
        
        
    def test_update_wrong_max_area_overflow_negative(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"]= {
                "id" : 3,
                "type": "admin",
                "company_id": 2
        }
        _vehicle = {
            "vehicle" : {
                "max_area" : -30.35
            }
        }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps(_vehicle), content_type='application/json')
        assert res.status_code == 400
        assert res.json == {'info': 'Bad request, some required fields are not recognized'}
        mocker.stopall()


    def test_update_success(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        def is_existing(conditions, **kwargs):
            return "id" in conditions

        mocker.patch.object(DBHandler, "is_existing", side_effect=is_existing)
        mocker.patch.object(DBHandler, "update", return_value=True)
        res = client.put(url_for("vehicle.update", id=12), data=json.dumps(self.vehicle),
                         content_type='application/json')
        assert res.status_code == 200
        assert res.json == {'info': "Vehicle updated successfully"}
        mocker.stopall()


########### DELETE ############
    def test_delete_unauthorized(self, mocker, client):
        res = client.delete(url_for("vehicle.delete", id=6))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_delete_wrong_vehicle(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.delete(url_for("vehicle.delete", id=6))
        assert res.status_code == 404
        assert res.json == {'info': 'Vehicle not found'}
        mocker.stopall()


    def test_delete_success(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "is_existing", return_value=True)
        mocker.patch.object(DBHandler, "delete", return_value=True)
        res = client.delete(url_for("vehicle.delete", id=6))
        assert res.status_code == 200
        assert res.json == {'info': 'Vehicle deleted successfully'}
        mocker.stopall()


    ############## GET ######################
    def test_get_unauthorized(self, client):
        res = client.get(url_for('vehicle.get', id=12))
        assert res.status_code == 401
        assert res.json == {"info": "Unauthorized access"}


    def test_get_with_wrong_params(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, 'select',  return_value=None)
        res = client.get(url_for('vehicle.get', id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Vehicle not found'}
        mocker.stopall()


    def test_get_with_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        vehicle = {
            "id" : 12,
            "registration" : "GHFDH546",
            "type" : "tractor",
            "max_weight" : 40.3,
            "max_area" : 34.45
        }
        mocker.patch.object(DBHandler, 'select', return_value=vehicle)
        res = client.get(url_for('vehicle.get', id=12))
        assert res.status_code == 200
        assert "vehicle" in res.json
        assert res.json["vehicle"] == vehicle
        mocker.stopall()
        

############## GET ALL ###############
    def test_getall_unauthorized(self, client):
        res = client.get(url_for("vehicle.getAll"))
        assert res.status_code == 401
        assert res.json == {"info": "Unauthorized access"}

    def test_getAll_with_no_vehicles(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "select", return_value=[])
        res = client.get(url_for("vehicle.getAll"))
        assert "vehicles" in res.json
        assert isinstance(res.json["vehicles"], list)
        assert len(res.json["vehicles"]) == 0
        assert res.status_code == 200
        mocker.stopall()


    def test_getAll_with_vehicles(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        _vehicle = {
            "id": 12,
            "registration": "GHFDH546",
            "type": "tractor",
            "max_weight": 40.3,
            "max_area": 34.45
        }

        mocker.patch.object(DBHandler, "select", return_value=[_vehicle,])
        res = client.get(url_for("vehicle.getAll"))
        assert "vehicles" in res.json
        assert isinstance(res.json["vehicles"], list)
        assert len(res.json["vehicles"]) == 1
        assert res.json["vehicles"][0] == {"vehicle":_vehicle}
        assert res.status_code == 200
        mocker.stopall()


