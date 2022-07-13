from datetime import datetime

from . import db


class BaseModel(db.Model):
    __abstract__ = True

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
                db.session.flush()
                db.session.refresh(self)
            except Exception as e:
                db.session.rollback()
                raise e
            return self


class Houmer(BaseModel):
    __tablename__ = 'houmer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), primary_key=True, nullable=False)


class RealState(BaseModel):
    __tablename__ = 'real_state'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), primary_key=True, nullable=False)
    latitude = db.Column(db.Float(precision=32), primary_key=True, nullable=False)
    longitude = db.Column(db.Float(precision=32), primary_key=True, nullable=False)


class HoumerPosition(BaseModel):
    __tablename__ = 'houmer_position'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    houmer_id = db.Column(db.Integer, db.ForeignKey(Houmer.id), primary_key=True)
    latitude = db.Column(db.Float(precision=32), nullable=False, primary_key=True)
    longitude = db.Column(db.Float(precision=32), nullable=False, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, primary_key=True)

    houmer = db.relationship('Houmer', foreign_keys='HoumerPosition.houmer_id')


class HoumerVisitRealState(BaseModel):
    __tablename__ = 'houmer_visit_real_state'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    houmer_id = db.Column(db.Integer, db.ForeignKey(Houmer.id), primary_key=True)
    real_state_id = db.Column(db.Integer, db.ForeignKey(RealState.id), primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, primary_key=True)
    end_date = db.Column(db.DateTime, nullable=False)

    houmer = db.relationship('Houmer', foreign_keys='HoumerVisitRealState.houmer_id')
    real_state = db.relationship('RealState', foreign_keys='HoumerVisitRealState.real_state_id')
