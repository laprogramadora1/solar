from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb              # <------- HERE!

db = SQLAlchemy()

def create_app():
    #"""Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    
    
    with app.app_context():
        #from . import routes  # Import routes
        from routes.api import api
        from routes.admin import admin
        app.register_blueprint(api)
        app.register_blueprint(admin)
        db.create_all()  # Create sql tables for our data models

        return app