from flask import Flask
from .module.db import initDB
from .module.auth import initJWT

 
def create_app(config_name):
 
    app = Flask(__name__, static_folder='static')
    initDB(app)
    initJWT(app)
    
    return app