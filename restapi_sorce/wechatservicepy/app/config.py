import os
from urllib.parse import quote_plus as urlquote
basedir = os.path.abspath(os.path.dirname(__file__))

is_development =True
redis_model = 0
database_model = 0

class Config:
    URL_PREFIX_SCH = ''
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    PORT = 8080

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 8887
    LOG_LEVEL = 10
    DEVELOPMENT = True
    KONG_AUTO_REGISTER = False
    CONSUL_AUTO_REGISTER = False
    LOGIN_USER_NAME = 'dev'
    LOGIN_USER_ID = '111'
    LOGIN_USER_SYSTEMUSER=True
    LOGIN_USER_COMPANYID = ''
    SYSTEM_NAME = ''
    SYSTEM_ID = ''
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:mysql123456789@localhost:3306/smartking'
    UPLOAD_FOLDER = 'C://files'
    REDIS_MODEL = 0
    REDIS_URL = 'redis://:localhost:6379/0'

    SESSION_EXPIRATION_TIME = 0

config = {
    'default': DevelopmentConfig
}
if __name__ == '__main__':
    conf = config['default']
    print(conf.PORT)
    print(config['default'].PORT)
