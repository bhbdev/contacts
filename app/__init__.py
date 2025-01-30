import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from markupsafe import escape
#from app.models import Contact
#from .helpers import t_path

from config import Config


db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def create_app(config_class=Config):    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)  
    migrate.init_app(app, db)
    moment.init_app(app)

    with app.app_context():
        db.create_all()
        if app.config['SEED_DB']:
            from app.helpers.seeder import seed_contacts
            seed_contacts(int(app.config['SEED_COUNT']) or 25)


    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.contacts import bp as contacts_bp
    app.register_blueprint(contacts_bp)

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/app.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Contacts startup')
    
    return app

from app import models

