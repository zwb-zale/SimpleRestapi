from app import db
from datetime import datetime,timedelta,date
import json
from enum import Enum
from flask import current_app
import decimal
import uuid

from app.time_util import date2str, datetime2isostr, get_locale_timezone


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o,datetime):
            return date2str(o)
        elif isinstance(o,datetime):
            if o.tzinfo is None:
                return datetime2isostr(o.astimezone(get_locale_timezone()))
            return datetime2isostr(o)
        super(DecimalEncoder, self).default(o)
class SqlType(Enum):
    mysql = 0
    mssql = 1
    sqlite = 2
def getSqlType():
    sql_uri =  current_app.config['SQLALCHEMY_DATABASE_URI']
    if sql_uri.startswith('mysql+mysqldb'):
        return SqlType.mysql.value
    elif sql_uri.startswith('mssql+pymssql'):
        return SqlType.mssql.value
    elif sql_uri.startswith('sqlite:'):
        return SqlType.sqlite.value
    else:
        assert False,'不能识别的SQL驱动,%s'%sql_uri

class Wechatphone_base(db.Model):
    __tablename__ = 'wechatphone'
    __table_args__ = {'implicit_returning': False}
    id = db.Column(db.Integer, primary_key=True)
    api = db.Column(db.String(500))
    api_type = db.Column(db.Integer)
    countrycode = db.Column(db.String(50))
    password = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    phone_code = db.Column(db.String(50))
    finish_state = db.Column(db.Integer)
    deviceid = db.Column(db.String(200))
    finish_deviceid = db.Column(db.String(200))
    bind_timestamp = db.Column(db.Integer)
    ppd = db.Column(db.String(100))
    def __repr__(self):
        return json.dumps(self.to_json(),cls = DecimalEncoder)
    def to_json(self,fields:list=None):
        return {key: getattr(self, key) for key in (fields or self.__table__.columns.keys())
                   if hasattr(self,key)
               }
