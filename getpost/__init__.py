from flask import Flask

from config import DevConfig
from desk.owls import owls_blueprint
from desk.parcels import parcels_blueprint
from desk.wizards import wizards_blueprint


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route('/')
    def index():
        return '<h1>What the brangan.</h1>'

    app.register_blueprint(owls_blueprint)
    app.register_blueprint(parcels_blueprint)
    app.register_blueprint(wizards_blueprint)

    return app


if __name__ == '__main__':
    app = create_app(DevConfig)
    app.run()
