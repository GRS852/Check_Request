import configparser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    CORS(app)

    config = configparser.ConfigParser()
    config.read("data/config.ini")
    config_dict = {key: value for key, value in config['webextract'].items()}
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config_dict["user"]}:{config_dict["password"]}@{config_dict["host"]}:{config_dict["port"]}/{config_dict["database"]}'
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)


    from . import routes
    routes.init_api(app)

    from . import ansync_route
    ansync_route.init_api(app)



    return app
