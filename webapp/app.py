import os
from flask import Flask, flash, g, render_template, request, redirect, session, url_for
from py.backuper import create_backup_zip
from py.day import alternance_day, what_day_month
from py.db import db
from py.model import Homework, Cour
from datetime import datetime, timedelta
from sys_lib_framework import display_uc, loading_defined, pdf_txt
from learning_routes import learning_bp
from admin import administrator
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BTS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'anykey'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

count = 0

#Error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error/500.html'), 500

# pdf_txt(file) -> save it into sources/test-prod/prod-courses

@app.context_processor
def inject_functions():
    """ Injecter des fonctions globales dans les templates """
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
    """ Page du terminal """
    return render_template('terminal.html')

@app.route('/about')
def about():
    """ Page à propos """
    return render_template('about.html')

# Enregistrement des blueprints
app.register_blueprint(learning_bp)
app.register_blueprint(administrator)


# Exécution de l'application
if __name__ == '__main__':
    
    # Initialiser la base de données avec l'application Flask
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # threading.Thread(target=display_uc).start()
    app.run(debug=True)
