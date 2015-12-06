class Config(object):
    DB_URI = 'postgresql+psycopg2://user:password@ip:port/db_name'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    DB_URI = 'postgresql+psycopg2://vulture@localhost:5432/vulture'


class TestConfig(Config):
    DEBUG = True
    TESTING = True
