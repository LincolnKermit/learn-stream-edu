import os, time
from flask import Blueprint, flash, redirect, render_template, session, url_for
from pyfile.mylib.backuper import create_backup_zip
from pyfile.db import db
from pyfile.config.model import Classe, Homework, Matiere, User
from datetime import datetime
from flask import request
from flask import session, redirect, url_for, flash
from decoration import admin_required
from werkzeug.security import generate_password_hash

pending_requests = {}

administrator = Blueprint('admin', __name__, template_folder='templates/admin')


@administrator.route('/admin/manage_users', methods=['GET', 'POST'])
@admin_required
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
            id_classe="0000000000",
            right="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Compte administrateur créé avec succès.")
"""


@administrator.route('/admin')
def admin():
    """ Affichage du panneau d'administration """
    matieres_nb = Matiere.query.count()
    nb_user = User.query.count()
    classes = Classe.query.all()
    if 'username' in session and session['right'] == 'admin':
        return render_template('admin/admin_panel.html', matieres_nb=matieres_nb, pending_requests=pending_requests, nb_user=nb_user, classes=classes)
    else:
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'error')
        time.sleep(0.5)
        return redirect(url_for('index'))

@administrator.route('/admin/all_lessons')
def all_lessons():
    # Récupérer tous les devoirs
    matiere = Matiere.query.all()
    return render_template('./learning/all_lessons.html', matieres=matiere)

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
        # Check if the user is in the pending requests
        if username in pending_requests:
            # Retrieve the user's information from the pending requests
            user_data = pending_requests.pop(username)

            # Retrieve form values
            existing_class_id = request.form.get('existingClass')
            new_class_name = request.form.get('newClass')

            # Determine the user's class
            if existing_class_id:
                id_class = existing_class_id
            elif new_class_name:
                # Create a new class if it doesn't exist
                new_class = Classe(nomClasse=new_class_name)
                db.session.add(new_class)
                try:
                    db.session.commit()  # Commit to get the ID
                    id_class = new_class.id
                except Exception as e:
                    db.session.rollback()  # Rollback if there's an error
                    flash("Erreur lors de la création de la classe : " + str(e), 'error')
                    return redirect(url_for('admin.admin'))
            else:
                flash("Veuillez sélectionner ou créer une classe.", 'error')
                return redirect(url_for('admin.admin'))

            # Create a new user and add to the database
            new_user = User(
                firstname=user_data['firstname'],
                lastname=user_data['lastname'],
                username=user_data['username'],
                mail=user_data['mail'],
                password=user_data['password'],  # Password should be hashed
                phoneNumber=user_data['phoneNumber'],
                date=user_data.get('date'),  # Use .get() to avoid KeyError
                id_classe=id_class,  # Assign the selected class
                right="user"  # Default rights: standard user
            )

            db.session.add(new_user)
            try:
                db.session.commit()  # Commit the new user
                flash(f"L'utilisateur {username} a été approuvé avec succès.", 'success')
            except Exception as e:
                db.session.rollback()  # Rollback on error
                flash("Erreur lors de l'approbation de l'utilisateur : " + str(e), 'error')

        else:
            flash(f"L'utilisateur {username} n'est pas dans la file d'attente.", 'error')

        return redirect(url_for('admin.admin'))
    else:
        flash("Vous n'avez pas l'autorisation d'effectuer cette action.", 'error')
        return redirect(url_for('users.login'))


@administrator.route('/admin/add_classe', methods=['GET', 'POST'])
def add_classe():
    """Permet à un administrateur d'ajouter une nouvelle classe."""
    if 'username' in session and session['right'] == 'admin':
        if request.method == 'POST':
            nom_classe = request.form['nomClasse']
            
            # Vérifie si une classe avec ce nom existe déjà
            existing_classe = Classe.query.filter_by(nomClasse=nom_classe).first()
            if existing_classe:
                flash('Une classe avec ce nom existe déjà.', 'error')
            else:
                # Crée une nouvelle classe
                new_classe = Classe(nomClasse=nom_classe)
                db.session.add(new_classe)
                try:
                    db.session.commit()
                    flash('Classe ajoutée avec succès.', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Erreur lors de l\'ajout de la classe : {str(e)}', 'error')

            return redirect(url_for('admin.add_classe'))

        return render_template('/classe/add_classe.html')
    else:
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'error')
        return redirect(url_for('index'))
