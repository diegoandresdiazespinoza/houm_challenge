import json

import requests


def test_houmer_insert():
    payload = {"name": "test unit 3", "email": "testunit3@email.cl"}
    headers = {"Content-Type": "application/json",
               "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8"}
    url = "http://localhost:5000/houm_challenge/houmer"
    request = requests.post(url=url, headers=headers, data=json.dumps(payload))
    response = json.loads(request.content)
    print(response)


test_houmer_insert()