import json
from unittest import TestCase
import requests


class HoumChallengeUnitTest(TestCase):
    headers = {"Content-Type": "application/json",
               "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8"}
    base_url = "http://localhost:5000/houm_challenge/"

    def send_request(self, url, payload, test_response):
        request = requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        self.assertTrue(request.content.decode("utf-8").__contains__(test_response))

    def test_houmer_insert(self):
        payload = {"name": "test unit 3", "email": "testunit3@email.cl"}
        url = f"{self.base_url}houmer"
        self.send_request(url, payload, "houmer inserted ok")

    def test_real_state_insert(self):
        payload = {"name": "Edificio 1", "latitude": -70.0, "longitude":-20.0}
        url = f"{self.base_url}real_state"
        self.send_request(url, payload, "real state inserted ok")

    def test_houmer_position_insert_1(self):
        payload = {"name": "test unit 3", "email": "testunit3@email.cl"}
        url = f"{self.base_url}houmer"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"houmer_id": 1, "latitude": -71.0, "longitude":-21.0, "date":"1997-07-14 10:00:00"}
        url = f"{self.base_url}houmer/position"
        self.send_request(url, payload, "position inserted ok")

    def test_houmer_visit_real_state(self):
        payload = {"name": "test unit 3", "email": "testunit3@email.cl"}
        url = f"{self.base_url}houmer"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"name": "Edificio 1", "latitude": -70.0, "longitude": -20.0}
        url = f"{self.base_url}real_state"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"houmer_id": 1, "real_state_id":1, "start_date":"1999-07-14 12:00:00", "end_date":"1999-07-14 13:43:00"}
        url = f"{self.base_url}houmer/visit"
        self.send_request(url, payload, "houmer visit real state inserted ok")

    def test_houmer_visit_coordinates(self):
        payload = {"name": "test unit 3", "email": "testunit3@email.cl"}
        url = f"{self.base_url}houmer"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"name": "Edificio 1", "latitude": -70.0, "longitude": -20.0}
        url = f"{self.base_url}real_state"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"houmer_id": 1, "real_state_id": 1, "start_date": "1999-07-14 12:00:00",
                   "end_date": "1999-07-14 13:43:00"}
        url = f"{self.base_url}houmer/visit"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"houmer_id": 1, "date":"1999-07-14"}
        url = f"{self.base_url}houmer/visit/coordinates"
        self.send_request(url, payload, '"latitude": -70.0, "longitude": -20.0, "spent_time": "1.0:43.0:0.0"')

    def test_houmer_exceeded_speed(self):
        payload = {"name": "test unit 3", "email": "testunit3@email.cl"}
        url = f"{self.base_url}houmer"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"name": "Edificio 1", "latitude": -70.0, "longitude": -20.0}
        url = f"{self.base_url}real_state"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"houmer_id": 1, "latitude": -70, "longitude": -20, "date": "1997-07-14 10:00:00"}
        url = f"{self.base_url}houmer/position"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"houmer_id": 1, "latitude": -70, "longitude": -20, "date": "1997-07-14 11:00:00"}
        url = f"{self.base_url}houmer/position"
        requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        payload = {"houmer_id": 1, "date": "1997-07-14", "max_speed": 0.0}
        url = f"{self.base_url}houmer/exceeded_speed"
        self.send_request(url, payload, '1997-07-14 10:00:00')


