from dotenv import load_dotenv, find_dotenv
import os

from flask import Flask
from flask import jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from pathlib import Path
from app import db, create_app
from helper import not_found_response

app = create_app(Path.cwd())
db.init_app(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# url error handler
@app.errorhandler(404)
def not_found(error=None):
    response = not_found_response(url=request.url)
    return response
app.run()