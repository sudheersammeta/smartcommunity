# app/teacher/__init__.py

from flask import Blueprint

teacher = Blueprint('teacher', __name__)

from . import views
