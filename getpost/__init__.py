from flask import Flask, render_template, send_from_directory
from os.path import join, dirname, abspath

from .desk.hogwarts import hogwarts_blueprint
from .desk.boats import boats_blueprint
from .desk.carriages import carriages_blueprint
from .desk.owls import owls_blueprint
from .desk.parcels import parcels_blueprint
from .desk.wizards import wizards_blueprint
from .desk.professors import professors_blueprint
from .desk.headmaster import headmaster_blueprint

from .desk.prefects import is_logged_in


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    register_blueprints(app)
    install_error_handlers(app)
    install_static_routers(app)
    install_jinja_globals(app)

    return app

def register_blueprints(app):
    for blueprint in {
        hogwarts_blueprint, boats_blueprint, carriages_blueprint,
        owls_blueprint, parcels_blueprint, wizards_blueprint,
        professors_blueprint, headmaster_blueprint
    }:
        app.register_blueprint(blueprint)

def install_error_handlers(app):
    @app.errorhandler(500)
    def internal(error):
        desc = 'Uh oh! Something went wrong.'
        return render_template(
            'voldemort.html', status=500, description=desc
        ), 500

    @app.errorhandler(404)
    def not_found(error):
        desc = 'This page does not exist.'
        return render_template(
            'voldemort.html', status=404, description=desc
        ), 404

    @app.errorhandler(403)
    def permission_denied(error):
        desc = 'You do not have permission to access this page.'
        return render_template(
            'voldemort.html', status=403, description=desc
        )

def install_static_routers(app):
    static_directory = join(abspath(dirname(__file__)), 'static/')

    css_codenames = {'template.css': 'maraudersmap.css',
                     'error.css': 'voldemort.css',
                     'home.css': 'hogwarts.css',
                     'forms.css': 'scrolls.css',
                     'edituser.css': 'transfigure.css'}

    @app.route('/css/<path:path>')
    def send_css(path):
        if path in css_codenames:
            path = css_codenames[path]
        return send_from_directory(join(static_directory, 'css/'), path)


    js_codenames = {'signup.js': 'boats.js'}

    @app.route('/js/<path:path>')
    def send_js(path):
        if path in js_codenames:
            path = js_codenames[path]
        return send_from_directory(join(static_directory, 'js/'), path)

def install_jinja_globals(app):
    app.jinja_env.globals.update(is_logged_in=is_logged_in)
