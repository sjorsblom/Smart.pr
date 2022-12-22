"""Main constructor file for flask setup

This module contains:
- Database initialization
- Security Policies
- Response Headers
- CORS
- Blueprint Registration
"""

import os

from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_talisman import Talisman
from app.config import config

##########################################
# Instantiate the extensions
##########################################

db = MongoEngine()

def create_app(config_name=None):
    ##########################################
    # Instantiate the app
    ##########################################
     
    app = Flask(__name__)
    
    ##########################################
    # Check and apply config
    ##########################################
       
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "production")
    
    app.config.from_object(config[config_name])

    ##########################################
    # Set up extensions
    ##########################################
    
    db.init_app(app)
    
    ##########################################
    # HTTP(S) Security Headers
    ##########################################

    csp = {
        'default-src': ['\'self\''],
        'frame-ancestors': ['\'none\'']
    }

    Talisman(
        app,
        force_https=False,
        frame_options='DENY',
        content_security_policy=csp,
        referrer_policy='no-referrer',
        x_xss_protection=False,
        x_content_type_options=True
    )

    @app.after_request
    def add_headers(response):
        response.headers['X-XSS-Protection'] = '0'
        response.headers['Cache-Control'] = 'no-store, max-age=0, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    ##########################################
    # CORS
    ##########################################

    CORS(app, resources={r"*": {"origins": "*"}})
    
    ##########################################
    # Blueprints
    ##########################################

    ##########################################
    # Shell context for flask cli
    ##########################################
    
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
