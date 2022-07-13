import datetime
from functools import wraps
import jwt as jwt
from flask import Flask, request, jsonify, make_response, current_app
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from app import app, db
from app.models import HoumerPosition, Houmer, HoumerVisitRealState, RealState


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        # print(jwt.encode({"user":"diego", "email":"test"}, app.config["SECRET_KEY"], algorithm='HS256'))
        # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return jsonify({'message': 'invalid token'})
        if data != {'user': 'diego', 'email': 'test'}:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)

    return decorator


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, current_app.config[schema_name])
            except ValidationError as e:
                return jsonify({"error": "invalid json schema"}), 400
            return f(*args, **kw)

        return wrapper

    return decorator


@app.route('/houm_challenge/status', methods=['POST', 'GET'])
@token_required
def status():
    print("hola")
    return make_response('api status ok', 200)


@app.route('/houm_challenge/houmer/', methods=['POST'])
@token_required
@validate_schema("HOUMER_SCHEMA")
def add_houmer():
    email = request.json["email"]
    name = request.json['name']
    houmer = Houmer(name=name, email=email)
    houmer.save()
    houmer_id = houmer.id
    return make_response({"status":"ok", "message":f"houmer inserted ok. id:{houmer_id}"}, 200)

@app.route('/houm_challenge/houmer/position/', methods=['POST'])
@token_required
@validate_schema("POSITION_SCHEMA")
def add_houmer_position():
    houmer_id = request.json['houmer_id']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    date = None
    if "date" in request.json:
        date = request.json['date']
    houmer_position = HoumerPosition(houmer_id=houmer_id, latitude=latitude, longitude=longitude, date=date)
    houmer_position.save()
    houmer_position_id = houmer_position.id
    return make_response({"status":"ok", "message":f"houmer position inserted ok. id:{houmer_position_id}"}, 200)

@app.route('/houm_challenge/houmer/visit/', methods=['POST'])
@token_required
@validate_schema("HOUMER_VISIT_REAL_STATE_SCHEMA")
def add_houmer_visit_real_state():
    houmer_id = request.json['houmer_id']
    real_state_id = request.json['real_state_id']
    start_date = request.json['end_date']
    end_date = request.json['start_date']
    houmer_visit_real_state = HoumerVisitRealState(houmer_id=houmer_id, real_state_id=real_state_id, start_date=start_date, end_date=end_date)
    houmer_visit_real_state.save()
    houmer_visit_real_state_id = houmer_visit_real_state.id
    return make_response({"status":"ok", "message":f"houmer visit real state inserted ok. id:{houmer_visit_real_state_id}"}, 200)

@app.route('/houm_challenge/real_state/', methods=['POST'])
@token_required
@validate_schema("REAL_STATE_SCHEMA")
def add_real_state():
    name = request.json['name']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    real_state = RealState(name=name, latitude=latitude, longitude=longitude)
    real_state.save()
    real_state_id = real_state.id
    return make_response({"status":"ok", "message":f"real state inserted ok. id:{real_state_id}"}, 200)