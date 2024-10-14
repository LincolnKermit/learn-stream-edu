# extensions.py
from pyfile.config.config import Config
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)
