from flask import Blueprint
import os
from models.database import SpotifyDB 

# USED FOR TESTING ---------------------------------------------------------
services = Blueprint('services', __name__, url_prefix='/services')
@services.route('/cleanup')
def cleanup():
    db.cleanup()
    return "Database cleaned up"

@services.route('/shutdown')
def shutdown():
    os._exit(0)
    return ""


