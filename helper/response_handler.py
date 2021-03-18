from flask import jsonify

def ok_response(data=[], message="Data was fetched"):
    if data:
        response = jsonify({
                        "status": True,
                        "message": message,
                        "data": data
                    }), 200
    else:
        response = jsonify({
                        "status": False,
                        "message": "Data is empty",
                        "data": data
                    }), 200
    return response

def created_response(data=[], message="Data was created"):
    if data:
        response = jsonify({
                        "status": True,
                        "message": message,
                        "data": data
                    }), 201
    else:
        response = jsonify({
                        "status": True,
                        "message": message
                    }), 201
    return response

def updated_response(message="Data was updated"):
    response = jsonify({
                        "status": True,
                        "message": message
                    }), 200
    return response

def deleted_response(message="Data was deleted"):
    response = jsonify({
                        "status": True,
                        "message": message
                    }), 202
    return response

def unauthorized_response(required_data=[], message="Authorization is failed"):
    if required_data:
        response = jsonify({
                        "status": True,
                        "message": message,
                        "required_data": required_data
                    }), 401
    else:
        response = jsonify({
                        "status": False,
                        "message": message
                    }), 401
    return response

def forbidden_response(required_data=[], message="Access forbidden"):
    if required_data:
        response = jsonify({
                        "status": True,
                        "message": message,
                        "required_data": required_data
                    }), 403
    else:
        response = jsonify({
                        "status": False,
                        "message": message
                    }), 403
    return response

def badrequest_response(required_data=[], message="Bad request"):
    if required_data:
        response = jsonify({
                            "status": False,
                            "message": message,
                            "required_data": required_data
                        }), 400
    else:
        response = jsonify({
                            "status": False,
                            "message": message
                        }), 400
    return response

def not_found_response(url=None, message="This url not found"):
    if url:
        response = jsonify({
                            "status": False,
                            "url": url,
                            "message": message
                        }), 404
    else:
        response = jsonify({
                            "status": False,
                            "message": message
                        }), 404
    return response

def server_error_response(message="Request failed to process"):
    response = jsonify({
                        "status": False,
                        "message": message
                    }), 500
    return response