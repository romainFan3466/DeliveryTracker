
from flask import url_for, session
import pytest_mock
#from unittest.mock import patch
import pytest
from application.core.DBHandler import DBHandler
from werkzeug.datastructures import FileStorage
from application.controllers.deliveryController import get_all_deliveries
from application.classes.Delivery import Delivery
import json, datetime, os, simplejson


class TestBlueprintAssignment:

    with open('/home/romain/Documents/DeliveryTrackerProject/API/application/test/deliveryData.json') as data_file:
        deliveries = simplejson.load(data_file)
        # deliveries = deliveries["deliveries"]



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