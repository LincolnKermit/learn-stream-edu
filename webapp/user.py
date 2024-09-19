from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from admin import pending_requests
from py.config.model import User
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint('users', __name__, template_folder='templates/user')




@users.route('/user')
def user():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    if 'username' in session:
        user = User.query.all(filter=(User.username == session["username"])).first()
        print("User: ", user)
        return render_template('/users/dashboard.html', user=user)
    else:
        return "Error Log: username not in session while username being in session."



@users.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        mail = request.form['mail']
        password = request.form['password']
        phone_number = request.form['phoneNumber']

        # Vérifier si l'utilisateur n'existe pas déjà dans la base de données ou dans la file d'attente
        existing_user = User.query.filter((User.username == username) | (User.mail == mail)).first()
        if existing_user or username in pending_requests:
            flash('Le nom d\'utilisateur ou l\'adresse mail existe déjà ou est en attente d\'approbation.', 'error')
        else:
            # Ajouter l'utilisateur à la file d'attente
            pending_requests[username] = {
                'firstname': firstname,
                'lastname': lastname,
                'username': username,
                'mail': mail,
                'password': generate_password_hash(password),  # Hachage du mot de passe
                'phoneNumber': phone_number,
                'date': datetime.today().date()
            }
            flash('Inscription réussie ! Votre compte est en attente d\'approbation par l\'administrateur.', 'success')

    return render_template('/users/sign_up.html')

@users.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur existe dans la base de données
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Si le mot de passe est correct, connecter l'utilisateur
            session['username'] = user.username
            session['right'] = user.right  # Stocker le droit de l'utilisateur (admin ou user)
            flash('Connexion réussie !', 'success')
            if user.right == 'admin':
                return redirect(url_for('admin.admin'))
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')

    return render_template('/users/login.html')

# Route pour déconnexion
@users.route('/user/logout')
def logout():
    # pop everything
    
    session.pop('username', None)
    return redirect(url_for('users.login'))
