from flask import jsonify, request
import sys
from datetime import datetime
import pytz

timezone = pytz.timezone('Asia/Jakarta')
datetime = datetime.now(timezone)

from helper import ok_response, created_response, updated_response, deleted_response, badrequest_response, server_error_response

from . import blueprints
from app import db
from app.models import book_model
from middleware import auth

# initialize blueprints to blueprint for routes
blueprint = blueprints["book"]

auth = auth.Auth()

# routes
@blueprint.route('/', methods=['GET'])
@auth.apikey_require
@auth.auth_require
@auth.role_require(role_account=['admin', 'super_admin'])
def read_all():
        try:
            query = book_model.BookModel.query.all()
            data = book_model.books_schema.dump(query)
            if data:
                response = ok_response(data=data)
            else:
                response = ok_response()
            return response
        except:
            print("Unexpected error:", sys.exc_info())
            response = server_error_response()
            return response

@blueprint.route('/<_id>', methods=['GET'])
@auth.apikey_require
@auth.auth_require
@auth.role_require(role_account=['admin', 'super_admin'])
def read_detail(_id):
        try:
            query = book_model.BookModel.query.get(_id)
            data = book_model.book_schema.dump(query)
            if data:
                response = ok_response(data=data)
            else:
                response = ok_response()
            return response
        except:
            print("Unexpected error:", sys.exc_info())
            response = server_error_response()
            return response

@blueprint.route('/', methods=['POST'])
@auth.apikey_require
@auth.auth_require
@auth.role_require(role_account=['admin', 'super_admin'])
def create():
        try:
            data_user = request.args.get('data_user')

            # get request body for multipart form data body
            body_form = dict(request.form)

            # get request body for json body
            body_json = request.get_json()
            
            body = {}
            if body_form:
                body = body_form
            
            if body_json:
                body = body_json

            validate_body = book_model.validator.validate(body)
            if validate_body:
                title = body['title']
                description = body['description']
                created_by = data_user['_id']

                data = book_model.BookModel(title=title, description=description, created_by=created_by)
                db.session.add(data)
                db.session.commit()
                response = created_response()
            else:
                schema = (book_model.schema).copy()
                required_data = {}
                for key in schema:
                    required_data[key] = schema[key].copy()
                    required_data[key]['position'] = "body"
                response = badrequest_response(required_data=required_data)
            return response
        except:
            print("Unexpected error:", sys.exc_info())
            response = server_error_response()
            return response

@blueprint.route('/<_id>', methods=['PUT'])
@auth.apikey_require
@auth.auth_require
@auth.role_require(role_account=['admin', 'super_admin'])
def update(_id):
        data_user = request.args.get('data_user')
        try:
            # get request body for multipart form data body
            body_form = dict(request.form)

            # get request body for json body
            body_json = request.get_json()
            
            body = {}
            if body_form:
                body = body_form
            
            if body_json:
                body = body_json

            validate_body = book_model.validator.validate(body)
            if validate_body:
                data = book_model.BookModel.query.get(_id)
                if hasattr(data, '_id'):
                    data.title = body['title']
                    data.description = body['description']
                    data.updated_at = datetime
                    data.updated_by = data_user['_id']

                    db.session.add(data)
                    db.session.commit()
                    response = updated_response()
                else:
                    required_data = {
                    "_id": {
                            "type": "integer",
                            "required": True,
                            "position": "query",
                            "description": f"data for _id ({_id}) not found"
                        }
                }
                response = badrequest_response(required_data=required_data)
            else:
                schema = (book_model.schema).copy()
                required_data = {}
                for key in schema:
                    required_data[key] = schema[key].copy()
                    required_data[key]['position'] = "body"
                response = badrequest_response(required_data=required_data)
            return response
        except:
            print("Unexpected error:", sys.exc_info())
            response = server_error_response()
            return response

@blueprint.route('/<_id>', methods=['DELETE'])
@auth.apikey_require
@auth.auth_require
@auth.role_require(role_account=['admin', 'super_admin'])
def delete(_id):
        try:
            data = book_model.BookModel.query.get(_id)
            if data:
                db.session.delete(data)
                db.session.commit()
                response = deleted_response()
            else:
                required_data = {
                    "_id": {
                            "type": "integer",
                            "required": True,
                            "position": "query",
                            "description": f"data for _id ({_id}) not found"
                        }
                }
                response = badrequest_response(required_data=required_data)
            return response
        except:
            print("Unexpected error:", sys.exc_info())
            response = server_error_response()
            return response
# /end routes