from werkzeug.datastructures import ImmutableMultiDict
from flask import jsonify, request
import sys
from datetime import datetime
import pytz

timezone = pytz.timezone('Asia/Jakarta')
datetime = datetime.now(timezone)

from helper import ok_response, created_response, updated_response, deleted_response, badrequest_response, server_error_response

from . import blueprints
from app import db
from app.models import user_model
from middleware import auth

# initialize blueprints to blueprint for routes
blueprint = blueprints["user"]

auth = auth.Auth()

# routes
@blueprint.route('/', methods=['GET'])
@auth.apikey_require
@auth.auth_require
@auth.role_require(role_account=['admin', 'super_admin'])
def read_all():
        try:
            query = user_model.UserModel.query.all()
            data = user_model.users_schema.dump(query)
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
            query = user_model.UserModel.query.get(_id)
            data = user_model.user_schema.dump(query)
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
            # get request body for multipart form data body
            body_form = dict(request.form)

            # get request body for json body
            body_json = request.get_json()
            
            body = {}
            if body_form:
                body = body_form
            
            if body_json:
                body = body_json

            validate_body = user_model.validator.validate(body)
            if validate_body:
                username = body['username']
                password = body['password']

                data = user_model.UserModel(username=username, password=password)
                db.session.add(data)
                db.session.commit()
                response = created_response()
            else:
                schema = (user_model.schema).copy()
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

            validate_body = user_model.validator.validate(body)
            if validate_body:
                data = user_model.UserModel.query.get(_id)
                if hasattr(data, '_id'):
                    data.title = body['title']
                    data.description = body['description']
                    data.updated_at = datetime

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
                schema = (user_model.schema).copy()
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
            data = user_model.UserModel.query.get(_id)
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