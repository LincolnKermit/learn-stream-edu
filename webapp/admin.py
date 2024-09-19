import os, time
from flask import Blueprint, flash, redirect, render_template, session, url_for
from py.backuper import create_backup_zip
from py.db import db
from py.config.model import Homework, Matiere, User
from datetime import datetime
from flask import request
from werkzeug.security import generate_password_hash
from functools import wraps
from flask import session, redirect, url_for, flash

pending_requests = {}

administrator = Blueprint('admin', __name__, template_folder='templates/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session and session.get('right') == 'admin':
            return f(*args, **kwargs)
        else:
            flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'error')
            return redirect(url_for('users.login'))
    return decorated_function

@administrator.route('/admin/manage_users', methods=['GET', 'POST'])
def manage_users():
    """ Affiche la liste des utilisateurs avec une option de recherche par ID, prénom, nom ou nom d'utilisateur """
    
    # Récupérer les différents critères de recherche
    search_query = request.args.get('search', '')
    
    # Si le champ est vide, on retourne tous les utilisateurs
    if search_query:
        # Recherche sur plusieurs colonnes : id, username, firstname, lastname
        users = User.query.filter(
            (User.id.ilike(f'%{search_query}%')) |
            (User.username.ilike(f'%{search_query}%')) |
            (User.firstname.ilike(f'%{search_query}%')) |
            (User.lastname.ilike(f'%{search_query}%'))
        ).all()
    else:
        users = User.query.all()

    return render_template('/users/manage_users.html', users=users)

@administrator.route('/admin/update_user/<int:id>', methods=['POST'])
def update_user(id):
    """ Met à jour les droits d'un utilisateur """
    user = User.query.get_or_404(id)
    new_right = request.form.get('right')

    if new_right in ['admin', 'user']:
        user.right = new_right
        db.session.commit()
        flash('Droits de l\'utilisateur mis à jour.', 'success')
    else:
        flash('Droits invalides.', 'error')

    return redirect(url_for('admin.manage_users'))

@administrator.route('/admin/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    """ Supprimer un utilisateur """
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression de l\'utilisateur : {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_users'))

@administrator.route('/admin/delete_homework/<int:id>', methods=['POST'])
def delete_homework(id):
    """ Supprimer un devoir """
    homework_to_delete = Homework.query.get_or_404(id)
    
    try:
        # Supprimer le devoir de la base de données
        db.session.delete(homework_to_delete)
        db.session.commit()
        flash('Devoir supprimé avec succès.', 'success')
        return redirect(url_for('index'))  # Rediriger vers la page d'accueil
    except Exception as e:
        flash(f"Erreur lors de la suppression : {str(e)}", 'error')
        return redirect(url_for('index'))

@administrator.route('/admin/add_homework', methods=['GET', 'POST'])
def add_homework():
    """ Ajouter un nouveau devoir """
    if request.method == 'POST':
        date_str = request.form['date']
        homework_text = request.form['homework']
        matiere = request.form['matiere']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_homework = Homework(date=date, text=homework_text, matiere=matiere)
            db.session.add(new_homework)
            db.session.commit()
            flash('Devoir ajouté avec succès.', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Format de date invalide.', 'error')
    
    return render_template('admin/add_homework.html')

"""
@administrator.before_request
def create_admin():
    # Vérifier si un administrateur existe déjà
    admin_exists = User.query.filter_by(right='admin').first()
    if not admin_exists:
        # Si aucun administrateur n'existe, en créer un
        admin_user = User(
            date=datetime.today().date(),
            firstname="00000000",
            lastname="000000000",
            username="admin",
            mail="admin@example.com",
            password=generate_password_hash("ninoubabou!22/06"),  # Mot de passe par défaut à changer
            phoneNumber="0000000000",
            right="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Compte administrateur créé avec succès.")
"""

@administrator.route('/admin/add_matiere', methods=['GET', 'POST'])
def add_matiere():
    """ Ajouter une nouvelle matière """
    if request.method == 'POST':
        # Récupérer les données du formulaire
        date_str = request.form.get('date')
        nomMatiere = request.form.get('nomMatiere')
        mainChemin = request.form.get('mainChemin')

        # Validation de la date
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Date invalide. Veuillez entrer une date au format AAAA-MM-JJ.', 'error')
            return render_template('admin/add_matiere.html')

        # Vérifier que tous les champs requis sont remplis
        if not nomMatiere or not mainChemin:
            flash('Tous les champs sont obligatoires.', 'error')
            return render_template('admin/add_matiere.html')

        # Créer une nouvelle instance de Matiere
        new_matiere = Matiere(
            date=parsed_date,
            nomMatiere=nomMatiere,
            mainChemin=mainChemin,
        )

        # Ajouter à la base de données
        try:
            # Créer le répertoire pour la matière si nécessaire
            os.makedirs(f"./templates/learning/{nomMatiere}/", exist_ok=True)
            db.session.add(new_matiere)
            db.session.commit()
            flash('La matière a été ajoutée avec succès.', 'success')
            return redirect(url_for('admin.all_lessons'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout de la matière : {str(e)}', 'error')

    return render_template('/admin/add_matiere.html')

@administrator.route('/admin')
def admin():
    """ Affichage du panneau d'administration """
    matieres_nb = Matiere.query.count()
    nb_user = User.query.count()
    if 'username' in session and session['right'] == 'admin':
        return render_template('admin/admin_panel.html', matieres_nb=matieres_nb, pending_requests=pending_requests, nb_user=nb_user)
    else:
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'error')
        time.sleep(0.5)
        return redirect(url_for('index'))

@administrator.route('/admin/all_homework')
def all_homework():
    # Récupérer tous les devoirs
    homeworks = Homework.query.all()
    return render_template('all_homework.html', homeworks=homeworks)

@administrator.route('/admin/all_lessons')
def all_lessons():
    # Récupérer tous les devoirs
    matiere = Matiere.query.all()
    return render_template('./learning/all_lessons.html', lessons=matiere)

@administrator.route('/admin/reject/<username>', methods=['POST'])
def reject_user(username):
    if 'username' in session and session['right'] == 'admin':
        # Vérifier si l'utilisateur est dans la file d'attente
        if username in pending_requests:
            # Supprimer l'utilisateur de la file d'attente
            pending_requests.pop(username)
            flash(f"L'utilisateur {username} a été rejeté avec succès.", 'success')
        else:
            flash(f"L'utilisateur {username} n'est pas dans la file d'attente.", 'error')

        return redirect(url_for('admin_panel'))
    else:
        flash("Vous n'avez pas l'autorisation d'effectuer cette action.", 'error')
        return redirect(url_for('users.login'))

@administrator.route('/admin/approve/<username>', methods=['POST'])
def approve_user(username):
    if 'username' in session and session['right'] == 'admin':
        # Vérifier si l'utilisateur est dans la file d'attente
        if username in pending_requests:
            # Récupérer les informations de l'utilisateur
            user_data = pending_requests.pop(username)

            # Créer un nouvel utilisateur et l'ajouter à la base de données
            new_user = User(
                firstname=user_data['firstname'],
                lastname=user_data['lastname'],
                username=user_data['username'],
                mail=user_data['mail'],
                password=user_data['password'],  # Le mot de passe est déjà haché
                phoneNumber=user_data['phoneNumber'],
                date=user_data['date'],
                right="user"  # Droits par défaut : utilisateur standard
            )
            db.session.add(new_user)
            db.session.commit()

            flash(f"L'utilisateur {username} a été approuvé avec succès.", 'success')
        else:
            flash(f"L'utilisateur {username} n'est pas dans la file d'attente.", 'error')

        return redirect(url_for('admin.admin'))
    else:
        flash("Vous n'avez pas l'autorisation d'effectuer cette action.", 'error')
        return redirect(url_for('users.login'))


@administrator.route('/admin/delete_matiere/<int:id>', methods=['POST'])
def delete_matiere(id):
    """ Supprimer une matière """
    matiere_to_delete = Matiere.query.get_or_404(id)  # Adjusted from 'Cour' to 'Matiere'
    try:
        try:
            os.remove(matiere_to_delete.mainChemin)
            create_backup_zip(matiere_to_delete.mainChemin, '/backup/lessons/')
        except Exception as e:
            print(e + " pas de fichier de cour à supprimer")
        
        # Supprimer la matière de la base de données
        db.session.delete(matiere_to_delete)
        db.session.commit()
        return redirect(url_for('admin.all_lessons'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression de la matière: {str(e)}', 'error')
        return redirect(url_for('admin.all_lessons'))