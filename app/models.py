
import datetime
from app import db


class WebExtract(db.Model):
    __tablename__ = 'webextract'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    domain = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

class RequestDetail(db.Model):
    __tablename__ = 'request_detail'

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, nullable=False)
    http_status_code = db.Column(db.Integer, nullable=False)
    type_scan = db.Column(db.String, nullable=False)
    on_off = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

class RequestDetailAsync(db.Model):
    __tablename__ = 'request_detail_async'

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, nullable=False)
    http_status_code = db.Column(db.Integer, nullable=False)
    type_scan = db.Column(db.String, nullable=False)
    on_off = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)





