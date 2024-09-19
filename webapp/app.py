import os
from flask import Config, Flask, flash, g, jsonify, render_template, request, redirect, session, url_for
from user import users
from py.backuper import create_backup_zip
from py.day import alternance_day, what_day_month
from py.db import db
from py.config.config import *
from py.config.model import Homework
from datetime import datetime, timedelta
from sys_lib_framework import display_uc, loading_defined, pdf_txt
from learning_routes import learning_bp
from admin import administrator
import threading

app = Flask(__name__)
app.config.from_object(Config)


count = 0

#Error page
@app.errorhandler(404)
def page_not_found(e):
    """Error page 404"""
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Error page 500"""
    return render_template('error/500.html'), 500

# pdf_txt(file) -> save it into sources/test-prod/prod-courses

@app.context_processor
def inject_functions():
    # Injecter des fonctions globales dans les templates
    return dict(what_day_month=what_day_month)

@app.route('/')
@app.route('/index')
def index():
    """ Affichage de la page d'accueil """
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    next_week_start = end_of_week + timedelta(days=1)
    next_week_end = next_week_start + timedelta(days=6)

    # Requête pour récupérer les devoirs jusqu'à la fin de la semaine prochaine
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
app.register_blueprint(learning_bp)
app.register_blueprint(administrator)
app.register_blueprint(users)


# Exécution de l'application
if __name__ == '__main__':
    
    # Initialiser la base de données avec l'application Flask
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # TODO threading.Thread(target=display_uc).start()
    app.run(debug=True)
