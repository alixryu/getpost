from flask import Flask, send_from_directory, render_template

from config import DevConfig
from desk.owls import owls_blueprint
from desk.parcels import parcels_blueprint
from desk.wizards import wizards_blueprint


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route('/')
    def index():
        return render_template('template.html')

    @app.route('/css/<path:path>')
    def sendcss(path):
        return send_from_directory('styles', path)

    @app.route('/js/<path:path>')
    def sendjs(path):
        return send_from_directory('scripts', path)

    app.register_blueprint(owls_blueprint)
    app.register_blueprint(parcels_blueprint)
    app.register_blueprint(wizards_blueprint)

    return app


if __name__ == '__main__':
    app = create_app(DevConfig)
    app.run()
