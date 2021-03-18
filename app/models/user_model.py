from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, ma
from cerberus import Validator

timezone = pytz.timezone('Asia/Jakarta')
datetime = datetime.now(timezone)

schema = {
    "username": {
        "type": "string",
        "required": True
    },
    "password": {
        "type": "string",
        "required": True
    },
    "role": {
        "type": "string",
        "required": True
    },
    "updated_at": {
        "type": "datetime"
    }
}

schema_auth = {
    "username": {
        "type": "string",
        "required": True
    },
    "password": {
        "type": "string",
        "required": True
    }
}

validator = Validator(schema)
validator_auth = Validator(schema_auth)

class UserModel(db.Model):
    __tablename__ = 'users'
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(250))
    role = db.Column(db.String(12), server_default='user')
    created_at = db.Column(db.DateTime, default=datetime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, username, password, role, updated_at=None):
        self.username = username
        self.role = role
        self.set_password(password)
        self.updated_at = updated_at

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# users schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('_id', 'username', 'password', 'role', 'created_at', 'updated_at')

# initialize UserModel
UserModel

# initialize the user schema
user_schema = UserSchema() # for single data
users_schema = UserSchema(many=True) # for many data