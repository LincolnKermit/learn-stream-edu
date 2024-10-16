"""_summary_
    This file is for all about user (signup, login, logout, profiles)

    @function user() to redirect to dashboard of the user
    @function signup() to sign up create a acount
    @function login() to login to acount
    @function logout() to logout of the acount

Returns:
    _type_: _description_
"""
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from admin import pending_requests
from pyfile.config.model import User
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint('users', __name__, template_folder='templates/user')




@users.route('/user/<username>')
def user(username):
    """
    Returns:
       String or templates: return string or a link to the templates of the dashboard
    """
    if 'username' not in session:
        return redirect(url_for('users.login'))

    # Récupération de l'utilisateur par nom d'utilisateur
    user = User.query.filter(User.username == username).first()
    
    if user is None:
        return "User not found", 404  # Gérer le cas où l'utilisateur n'existe pas

    # Si l'utilisateur est trouvé, vous pouvez vérifier si c'est le même que l'utilisateur connecté
    current_user = User.query.filter(User.username == session["username"]).first()
    
    if current_user:
        print("Current User: ", current_user)

    # Renvoyer le modèle du profil utilisateur
    return render_template('/users/profile.html', user=user, current_user=current_user)

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
            session['id_classe'] = user.id_classe # Ajouter l'ID de l'utilisateur à la session
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
