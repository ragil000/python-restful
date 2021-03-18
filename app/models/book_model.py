from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, ma
from cerberus import Validator

timezone = pytz.timezone('Asia/Jakarta')
datetime = datetime.now(timezone)

schema = {
    "title": {
        "type": "string",
        "required": True
    },
    "description": {
        "type": "string",
        "required": True
    },
    "created_by": {
        "type": "integer",
        "required": True
    },
    "updated_at": {
        "type": "datetime"
    },
    "updated_by": {
        "type": "integer"
    }
}

validator = Validator(schema)

class BookModel(db.Model):
    __tablename__ = 'books'
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime)
    created_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer)

    def __init__(self, title, description, created_by, updated_at=None, updated_by=None):
        self.title = title
        self.description = description
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


# book schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('_id', 'title', 'description', 'created_at', 'created_by', 'updated_at', 'updated_by')

# initialize BookModel
BookModel

# initialize the user schema
book_schema = BookSchema() # for single data
books_schema = BookSchema(many=True) # for many data