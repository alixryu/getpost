from flask import Flask

from config import DevConfig
from floors.lobby import lobby_blueprint


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route('/')
    def index():
        return '<h1>What the brangan.</h1>'

    app.register_blueprint(lobby_blueprint)

    return app


if __name__ == '__main__':
    app = create_app(DevConfig)
    app.run()
