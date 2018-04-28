# app/student/__init__.py

from flask import Blueprint

parent = Blueprint('parent', __name__)

from . import views
