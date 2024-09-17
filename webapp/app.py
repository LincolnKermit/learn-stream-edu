import os
from flask import Flask, flash, g, jsonify, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from py.backuper import create_backup_zip
from py.day import alternance_day, what_day_month
from py.db import db
from py.model import Homework, Cour, User
from datetime import datetime, timedelta
from sys_lib_framework import display_uc, loading_defined, pdf_txt
from learning_routes import learning_bp
from admin import administrator, pending_requests
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
    """Error page 404"""
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Error page 500"""
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

# Route pour la page d'inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vérifier si l'utilisateur n'est pas déjà dans la base de données ou en attente d'approbation
        if not User.query.all() and username not in pending_requests:
            # Ajouter à la file d'attente pour approbation
            pending_requests[username] = {
                'username': username,
                'password': generate_password_hash(password),
            }
            flash('Inscription réussie ! Veuillez attendre que votre compte soit approuvé par l\'administrateur.')
        else:
            flash('Ce nom d\'utilisateur existe déjà ou est en attente d\'approbation.')
    return render_template('signup.html')

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    """login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(username)
        # Vérification si l'utilisateur est approuvé et les identifiants sont corrects
        if  user and check_password_hash(user.password, password):
            if user['approved']:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash("Votre compte n'est pas encore approuvé par l'administrateur.")
        else:
            flash('Identifiant ou mot de passe incorrect.')
    return render_template('login.html')

# Route pour déconnexion
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

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
