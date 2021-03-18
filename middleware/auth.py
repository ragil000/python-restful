from werkzeug.datastructures import ImmutableMultiDict
from flask import request, jsonify
import json
import jwt
from dotenv import load_dotenv, find_dotenv
import sys, os
from functools import wraps
from .crypto_rmy import decrypt_fernet
import ast

load_dotenv(find_dotenv())

class Auth():
    def apikey_require(self, f):
        def decorator(*args, **kwargs):
            header = request.headers
            if not header.get('X-API-KEY'):
                return jsonify({
                    "status": False,
                    "message": "API Key tidak ditemukan."
                }), 403

            apikey = header.get('X-API-KEY')
            if apikey != os.getenv('API_KEY'):
                return jsonify({
                    "status": False,
                    "message": "API Key tidak sah."
                }), 403
            return f(*args, **kwargs)
        decorator.__name__ = f.__name__
        return decorator

    def auth_require(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            header = request.headers
            
            if not header.get('Authorization'):
                return jsonify({
                    "status": False,
                    "message": "Need \"Authorization\""
                }), 403

            token = header.get('Authorization')
            token = token.split()

            if len(token) > 1:
                if token[0] != 'Bearer':
                    return jsonify({
                        "status": False,
                        "message": "Need \"Bearer\""
                    }), 403
                elif not token[1]:
                    return jsonify({
                        "status": False,
                        "message": "Missing token"
                    }), 403
                try:
                    data = jwt.decode(token[1], os.getenv('JWT_TOKEN'), algorithms='HS256')
                    sub = data['data_user']
                    decrypt = decrypt_fernet(sub.encode())

                    http_args = request.args.to_dict()
                    http_args['data_user'] = ast.literal_eval(decrypt)
                    request.args = ImmutableMultiDict(http_args)
                except:
                    print("Unexpected error:", sys.exc_info())
                    return jsonify({
                        "status": False,
                        "message": "Token not valid"
                    }), 403
            else:
                return jsonify({
                    "status": False,
                    "message": "Token not found"
                }), 403
            return f(*args, **kwargs)
        decorator.__name__ = f.__name__
        return decorator

    def role_require(self, role_account=[]):
        def decorator(f):
            @wraps(f)
            def check_role(*args, **kwargs):
                data_user = request.args.get('data_user')
                if not data_user:
                    return jsonify({
                        "status": False,
                        "message": "Data user session is missing"
                    }), 401
                if isinstance(data_user, dict):
                    if data_user['role'] not in role_account:
                        return jsonify({
                            "status": False,
                            "message": "Level not valid"
                        }), 403
                else:
                    return jsonify({
                        "status": False,
                        "message": "Format data user session is wrong"
                    }), 403
                return f(*args, **kwargs)
            check_role.__name__ = f.__name__
            return check_role
        return decorator