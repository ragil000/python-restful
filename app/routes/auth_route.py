from werkzeug.datastructures import ImmutableMultiDict
from flask import jsonify, request
import sys
import os
from datetime import datetime, timedelta, timezone
import pytz

timezone = pytz.timezone('Asia/Jakarta')
datetime = datetime.now(timezone)

from helper import ok_response, created_response, updated_response, deleted_response, badrequest_response, server_error_response

import jwt

from . import blueprints
from app import db
from app.models import user_model
from middleware import auth
from middleware.crypto_rmy import encrypt_fernet

auth = auth.Auth()
# initialize blueprints to blueprint for routes
blueprint = blueprints["auth"]

# routes
@blueprint.route('/', methods=['POST'])
@auth.apikey_require
def sign_in():
        try:
            schema = (user_model.schema_auth).copy()
            required_data = {}
            for key in schema:
                required_data[key] = schema[key].copy()
                required_data[key]['position'] = "body"

            # get request body for multipart form data body
            body_form = dict(request.form)

            # get request body for json body
            body_json = request.get_json()
            
            body = {}
            if body_form:
                body = body_form
            
            if body_json:
                body = body_json

            validate_body = user_model.validator_auth.validate(body)
            if validate_body:
                username = body['username']
                password = body['password']

                data = user_model.UserModel.query.filter_by(username=username).first()
                if hasattr(data, '_id'):
                    check_password = data.check_password(password)
                    if check_password:
                        secretKey = os.getenv('JWT_TOKEN')
                        data_user = {
                            "_id": data._id,
                            "username": data.username,
                            "role": data.role
                        }
                        encrypt = encrypt_fernet(str(data_user))
                        payload = {
                            "exp": datetime.utcnow() + timedelta(days=365),
                            "iat": datetime.utcnow(),
                            "data_user": encrypt.decode()
                        }
                        encoded_jwt = jwt.encode(payload, secretKey, algorithm='HS256')
                        data_user['token'] = encoded_jwt
                        response = ok_response(data=data_user)
                    else:
                        required_data['password']["description"] = "password is wrong"
                        response = badrequest_response(required_data=required_data)
                else:
                    required_data['username']["description"] = "username is wrong"
                    response = badrequest_response(required_data=required_data)
            else:
                response = badrequest_response(required_data=required_data)
            return response
        except:
            print("Unexpected error:", sys.exc_info())
            response = server_error_response()
            return response

@blueprint.route('/signup', methods=['POST'])
@auth.apikey_require
def sign_up():
        try:
            schema = (user_model.schema_auth).copy()
            required_data = {}
            for key in schema:
                required_data[key] = schema[key].copy()
                required_data[key]['position'] = "body"

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
                role = body['role']
                
                check_username = user_model.UserModel.query.filter_by(username=username).first()
                if hasattr(check_username, '_id'):
                    required_data['username']["unique"] = True
                    required_data['username']["description"] = "username is exists"
                    response = badrequest_response(required_data=required_data)
                else:
                    data = user_model.UserModel(username=username, password=password, role=role)
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
# /end routes