from flask import Flask, Blueprint


lobby = Blueprint('lobby', __name__, url_prefix='/lobby')

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>What the brangan.</h1>'


@lobby.route('/')
def lobby_index():
    return '<h1>Welcome to the Firelands lobby.</h1>'


app.register_blueprint(lobby)


if __name__ == '__main__':
    app.run(debug=True)
