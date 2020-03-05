# coding:utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))
host = "127.0.0.1"#os.getenv("mysqlhost")
password = os.getenv("mysqlpassword")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:{}@{}/nCov?charset=utf8".format(password, host)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:{}@{}/nCov?charset=utf8".format(password, host)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:{}@{}/nCov?charset=utf8".format(password, host)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "develop": DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    "default": DevelopmentConfig
}
