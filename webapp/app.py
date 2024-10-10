from flask import Flask, flash, g, jsonify, render_template, request, redirect, send_from_directory, session, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_sqlalchemy import SQLAlchemy
from user import users
from pyfile.mylib.backuper import create_backup_zip
from pyfile.mylib.day import alternance_day, what_day_month
from pyfile.db import db, db_messages
from pyfile.config.config import *
from pyfile.config.model import Classe, Homework
from datetime import datetime, timedelta
from learning_routes import learning_bp
from admin import administrator
from homework import homework
from chat import chat

import os
import eventlet
import eventlet.wsgi


app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app)
rooms = {}  # To track rooms and their participants


# Error pages
@app.errorhandler(404)
def page_not_found(e):
    """Error page 404"""
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Error page 500"""
    return render_template('error/500.html'), 500


@app.context_processor
def inject_user():
    user = session.get('username')  # Récupère l'utilisateur depuis la session
    return dict(user=user)


# Injecter des fonctions globales dans les templates
@app.context_processor
def inject_functions():
    return dict(what_day_month=what_day_month)


# Routes
@app.route('/')
@app.route('/index')
def index():
    """ Affichage de la page d'accueil """
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    next_week_start = end_of_week + timedelta(days=1)
    next_week_end = next_week_start + timedelta(days=6)

    homeworks = Homework.query.filter(Homework.date >= today, Homework.date <= next_week_end).order_by(Homework.date.asc()).all()

    return render_template('index.html', homeworks=homeworks, week=alternance_day())


@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/link')
def utils_link():
    return render_template('utils_link.html')




# Enregistrement des blueprints
app.register_blueprint(chat)
app.register_blueprint(learning_bp)
app.register_blueprint(administrator)
app.register_blueprint(users)
app.register_blueprint(homework)


# Exécution de l'application avec SocketIO
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.create_all('messages')
    
    # Utilisation de socketio.run au lieu de app.run pour SocketIO
    socketio.run(app, debug=True)
