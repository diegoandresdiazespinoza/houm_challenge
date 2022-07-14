import datetime
import json
import os
from functools import wraps

import haversine as haversine
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
            data = jwt.decode(token, os.getenv("API_SECRET_KEY"), algorithms=['HS256'])
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
                try:
                    json.dumps(request.json)
                except Exception as e:
                    return jsonify({"error": "no valid payload"}), 400
                validate(request.json, current_app.config[schema_name])
            except ValidationError as e:
                return jsonify({"error": "invalid schema"}), 400
            return f(*args, **kw)

        return wrapper

    return decorator


@app.route('/houm_challenge/status', methods=['POST', 'GET'])
@token_required
def status():
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
    return make_response({"message": f"houmer inserted ok. id:{houmer_id}"}, 200)


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
    return make_response({"message": f"houmer position inserted ok. id:{houmer_position_id}"}, 200)


@app.route('/houm_challenge/houmer/visit/', methods=['POST'])
@token_required
@validate_schema("HOUMER_VISIT_REAL_STATE_SCHEMA")
def add_houmer_visit_real_state():
    houmer_id = request.json['houmer_id']
    real_state_id = request.json['real_state_id']
    start_date = request.json['end_date']
    end_date = request.json['start_date']
    houmer_visit_real_state = HoumerVisitRealState(houmer_id=houmer_id, real_state_id=real_state_id,
                                                   start_date=start_date, end_date=end_date)
    houmer_visit_real_state.save()
    houmer_visit_real_state_id = houmer_visit_real_state.id
    return make_response({"message": f"houmer visit real state inserted ok. id:{houmer_visit_real_state_id}"}, 200)


@app.route('/houm_challenge/houmer/visit/coordinates', methods=['POST'])
@token_required
@validate_schema("HOUMER_VISIT_COORDINATES_SCHEMA")
def get_real_state_coordinates_visit():
    houmer_id = int(request.json["houmer_id"])
    start_date = datetime.datetime.strptime(request.json["date"], "%Y-%m-%d").replace(hour=0, minute=0, second=0)
    end_date = datetime.datetime.strptime(request.json["date"], "%Y-%m-%d").replace(hour=23, minute=59, second=59)
    visits: list[HoumerVisitRealState] = db.session.query(HoumerVisitRealState).filter(
        HoumerVisitRealState.houmer_id == houmer_id, HoumerVisitRealState.start_date >= start_date,
        HoumerVisitRealState.start_date <= end_date).all()
    visit_output = []
    for visit in visits:
        real_state: RealState = db.session.query(RealState).filter(RealState.id == visit.real_state_id).first()
        spent_timedelta = visit.end_date - visit.start_date
        seconds = spent_timedelta.total_seconds()
        hours = str(seconds // 3600)
        minutes = str((seconds % 3600) // 60)
        seconds = str(seconds % 60)
        spent_time = f"{hours}:{minutes}:{seconds}"
        real_state_coordinates = {"latitude": real_state.latitude, "longitude": real_state.longitude,
                                  "spent_time": spent_time}
        visit_output.append(real_state_coordinates)
    return make_response(json.dumps(visit_output), 200)


@app.route('/houm_challenge/houmer/exceeded_speed', methods=['POST'])
@token_required
@validate_schema("HOUMER_EXCEEDED_SPEED_SCHEMA")
def get_houmer_exceeded_speed():
    houmer_id = request.json["houmer_id"]
    max_speed = float(request.json["max_speed"])
    start_date = datetime.datetime.strptime(request.json["date"], "%Y-%m-%d").replace(hour=0, minute=0, second=0)
    end_date = datetime.datetime.strptime(request.json["date"], "%Y-%m-%d").replace(hour=23, minute=59, second=59)
    moments: list[HoumerPosition] = db.session.query(HoumerPosition).filter(HoumerPosition.houmer_id == houmer_id,
                                                                            HoumerPosition.date >= start_date,
                                                                            HoumerPosition.date <= end_date).order_by(
        HoumerPosition.date).all()
    index = 0
    speed_exceeded = []
    for moment in moments:
        index += 1
        if index >= len(moments):
            break
        next_moment = moments[index]
        spent_time = next_moment.date - moment.date
        distance = haversine.haversine((moment.latitude, moment.longitude),
                                       (next_moment.latitude, next_moment.longitude))
        speed = distance / (spent_time.total_seconds() / 3600.0)
        if speed >= max_speed:
            speed_exceeded.append(moment.date.strftime("%Y-%m-%d %H:%M:%S"))
    return make_response(json.dumps(speed_exceeded), 200)


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
    return make_response({"message": f"real state inserted ok. id:{real_state_id}"}, 200)
