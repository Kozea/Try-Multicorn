from flask import Flask
from log_colorizer import make_colored_stream_handler
from logging import getLogger, INFO, WARN
from mcdemo.db import db
from mcdemo import routes

import os

ROOT = os.path.dirname(__file__)

def app():
    """Initializes the mcdemo application"""
    static_folder = os.path.join(ROOT, 'static')
    template_folder = os.path.join(ROOT, 'templates')
    from mcdemo import config
    app = Flask(__name__,
                static_folder=static_folder,
                template_folder=template_folder)
    app.config.update(config.CONFIG)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.CONFIG["DB_URL"]
    app.config['SQLALCHEMY_BINDS'] = {
        'admin': config.CONFIG["DB_URL_ADMIN"]
    }
    db.init_app(app)
    handler = make_colored_stream_handler()
    getLogger('werkzeug').addHandler(handler)
    getLogger('werkzeug').setLevel(INFO)
    getLogger('sqlalchemy').addHandler(handler)
    getLogger('sqlalchemy').setLevel(INFO if app.debug else WARN)

    app.logger.handlers = []
    app.logger.addHandler(handler)
    routes.register(app)
    return app
