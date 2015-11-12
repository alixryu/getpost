from flask import Flask

from config import DevConfig
from floors.lobby import lobby_blueprint


app = Flask(__name__)
app.config.from_object(DevConfig)


@app.route('/')
def index():
    return '<h1>What the brangan.</h1>'


app.register_blueprint(lobby_blueprint)


if __name__ == '__main__':
    app.run()
