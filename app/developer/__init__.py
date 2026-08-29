from flask import Blueprint

developer = Blueprint('developer', __name__)

from app.developer import routes
