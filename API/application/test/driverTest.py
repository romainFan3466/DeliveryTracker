from flask import url_for
from application.core.DBHandler import DBHandler
import json
from decimal import Decimal


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
        
    
    ########### DELETE ############
    def test_delete_unauthorized(self, mocker, client):
        res = client.delete(url_for("driver.delete", id=6))
        assert res.status_code == 401
        assert res.json == {'info': 'Unauthorized access'}


    def test_delete_wrong_driver(self, mocker, client):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "is_existing", return_value=False)
        res = client.delete(url_for("driver.delete", id=6))
        assert res.status_code == 404
        assert res.json == {'info': 'Driver not found'}
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
        res = client.delete(url_for("driver.delete", id=6))
        assert res.status_code == 200
        assert res.json == {'info': 'Driver deleted successfully'}
        mocker.stopall()
        
    
     ############## GET ######################
    def test_get_unauthorized(self, client):
        res = client.get(url_for('driver.get', id=12))
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
        res = client.get(url_for('driver.get', id=12))
        assert res.status_code == 404
        assert res.json == {'info': 'Driver not found'}
        mocker.stopall()


    def test_get_with_success(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        _sql = {
            "id" : 2,
            "name": "Romain",
            "email": "romain@test.ie",
            "phone" : "5464654645",
            "location_lat" : 12.46666,
            "location_lng" : 13.46666
        }
        driver = {
            "id" : 2,
            "name": "Romain",
            "email": "romain@test.ie",
            "phone" : "5464654645",
            "location": {
                    "lat": 12.46666,
                    "lng": 13.46666
                }
        }
        mocker.patch.object(DBHandler, 'select', return_value=_sql)
        res = client.get(url_for('driver.get', id=12))
        assert res.status_code == 200
        assert "driver" in res.json
        assert res.json["driver"] == driver
        mocker.stopall()


############## GET ALL ###############
    def test_getall_unauthorized(self, client):
        res = client.get(url_for("driver.getAll"))
        assert res.status_code == 401
        assert res.json == {"info": "Unauthorized access"}

    def test_getAll_with_no_drivers(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }
        mocker.patch.object(DBHandler, "select", return_value=[])
        res = client.get(url_for("driver.getAll"))
        assert "drivers" in res.json
        assert isinstance(res.json["drivers"], list)
        assert len(res.json["drivers"]) == 0
        assert res.status_code == 200
        mocker.stopall()


    def test_getAll_with_drivers(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }


        _sql = [{
            "id": 2,
            "name": "Romain",
            "email": "romain@test.ie",
            "phone": "5464654645",
            "location_lat": Decimal(12.46666),
            "location_lng": Decimal(13.46666)
        }]
        driver = {
            "id": 2,
            "name": "Romain",
            "email": "romain@test.ie",
            "phone": "5464654645",
            "location": {
                "lat": Decimal(12.46666),
                "lng": Decimal(13.46666)
            }
        }

        mocker.patch.object(DBHandler, "select", return_value=_sql)
        res = client.get(url_for("driver.getAll"))
        assert "drivers" in res.json
        assert isinstance(res.json["drivers"], list)
        assert len(res.json["drivers"]) == 1
        assert res.json["drivers"][0] == {"driver":driver}
        assert res.status_code == 200
        mocker.stopall()


    def test_getAll_with_drivers_return_obj(self, client, mocker):
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 3,
                "type": "admin",
                "company_id": 2
            }

        _sql = [{
            "id": 2,
            "name": "Romain",
            "email": "romain@test.ie",
            "phone": "5464654645",
            "location_lat": Decimal(12.46666),
            "location_lng": Decimal(13.46666)
        }]
        driver = {
            "id": 2,
            "name": "Romain",
            "email": "romain@test.ie",
            "phone": "5464654645",
            "location": {
                "lat": Decimal(12.46666),
                "lng": Decimal(13.46666)
            }
        }

        from application.controllers.driverController import getAll
        mocker.patch.object(DBHandler, "select", return_value=_sql)
        res = getAll(return_obj=True)
        assert "drivers" in res.json
        assert isinstance(res.json["drivers"], list)
        assert len(res.json["drivers"]) == 1
        assert res.json["drivers"][0] == {"driver":driver}
        assert res.status_code == 200
        mocker.stopall()

