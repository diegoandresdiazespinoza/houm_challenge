from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Houmer(db.Model):
    __tablename__ = 'houmer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)


class HoumerPosition(db.Model):
    __tablename__ = 'houmer_position'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class RealState(db.Model):
    __tablename__ = 'real_state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


class HoumerVisitRealState(db.Model):
    __tablename__ = 'houmer_visit_real_state'
    houmer_id = db.Column(db.Integer, db.ForeignKey(Houmer.id), primary_key=True)
    real_state_id = db.Column(db.Integer, db.ForeignKey(RealState.id), primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    houmer = db.relationship('Houmer', foreign_keys='HoumerVisitRealState.houmer_id')
    real_state = db.relationship('RealState', foreign_keys='HoumerVisitRealState.real_state_id')
