import connexion
from app.config import config
from flask_cors import CORS
import logging
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from app.config import redis_model,database_model
import os

db = SQLAlchemy()

babel = Babel()

def apikey_auth(token, required_scopes):
    return {}

def create_app_swagger(config_name):
    conf = config[config_name]
    app_swg = connexion.App(__name__,
                            port = conf.PORT,
                            debug= conf.DEBUG,
                            specification_dir='../swagger/'
                            )
    app_swg.add_api('./v1_0/wechatservicepy.yaml', arguments={'title': 'api v1.0','host':os.environ.get('SWAGGER_HOST',f'localhost:{conf.PORT}')})
    app = app_swg.app
    CORS(app)
    app.config.from_object(conf)
    config[config_name].init_app(app)

    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    app.logger.addHandler(consoleHandler)
    app.logger.level = app.config['LOG_LEVEL']
    db.init_app(app)
    babel.init_app(app)
    return app_swg


