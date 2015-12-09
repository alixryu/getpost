from flask import Flask, send_from_directory, render_template

from config import DevConfig
from desk.hogwarts import hogwarts_blueprint
from desk.owls import owls_blueprint
from desk.parcels import parcels_blueprint
from desk.wizards import wizards_blueprint


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    app.register_blueprint(hogwarts_blueprint)
    app.register_blueprint(owls_blueprint)
    app.register_blueprint(parcels_blueprint)
    app.register_blueprint(wizards_blueprint)

    @app.errorhandler(500)
    def internal(error):
        title = 'Error 500'
        desc = 'Uh oh! Something went wrong.'
        return render_template('voldemort.html', title=title, description=desc), 500

    @app.errorhandler(404)
    def not_found(error):
        title = 'Error 404'
        desc = 'This page does not exist.'
        return render_template('voldemort.html', title=title, description=desc), 500

    return app


def main():
    app = create_app(DevConfig)
    app.run()

if __name__ == '__main__':
    main()
