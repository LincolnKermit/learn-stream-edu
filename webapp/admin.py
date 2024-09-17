import os
from flask import Blueprint, flash, redirect, render_template, session, url_for
from py.backuper import create_backup_zip
from py.db import db
from py.model import Homework, Cour
from datetime import datetime
from flask import request

pending_requests = {}

administrator = Blueprint('admin', __name__, template_folder='templates/admin')


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

@administrator.route('/admin/add_lessons', methods=['GET', 'POST'])
def add_lessons():
    """ Ajouter un nouveau cours """
    if request.method == 'POST':
        # Récupérer les données du formulaire
        date_str = request.form.get('date')
        nomCour = request.form.get('nomCour')
        matiere = request.form.get('matiere')
        mainChemin = request.form.get('mainChemin')
        idf = request.form.get('idf')

        # Validation de la date
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Date invalide. Veuillez entrer une date au format AAAA-MM-JJ.', 'error')
            return render_template('/learning/add_lessons.html')

        # Vérifier que tous les champs requis sont remplis
        if not nomCour or not matiere or not mainChemin or not idf:
            flash('Tous les champs sont obligatoires.', 'error')
            return render_template('/learning/add_lessons.html')

        # Créer une nouvelle instance de Cour
        new_cour = Cour(
            date=parsed_date,
            nomCour=nomCour,
            matiere=matiere,
            mainChemin=mainChemin,
            idf=idf
        )

        # Ajouter à la base de données
        try:
            db.session.add(new_cour)
            db.session.commit()
            flash('Le cours a été ajouté avec succès.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout du cours : {str(e)}', 'error')

    return render_template('/learning/add_lessons.html')





@administrator.route('/admin')
def admin():
    """ Affichage du panneau d'administration """
    cours_nb = Cour.query.count()
    return render_template('admin/admin_panel.html', cours_nb=cours_nb)

@administrator.route('/admin/all_homework')
def all_homework():
    # Récupérer tous les devoirs
    homeworks = Homework.query.all()
    return render_template('all_homework.html', homeworks=homeworks)

@administrator.route('/admin/all_lessons')
def all_lessons():
    # Récupérer tous les devoirs
    cours = Cour.query.all()
    return render_template('all_lessons.html', lessons=cours)


# Route pour approuver un utilisateur
@administrator.route('/approve/<username>')
def approve_user(username):
    if 'username' in session and session['username'] == 'admin':
        if username in pending_requests:
            # Déplacer l'utilisateur des requêtes en attente vers la base de données des utilisateurs
            users_db[username] = pending_requests.pop(username)
            flash(f'Utilisateur {username} approuvé avec succès !')
        else:
            flash(f"L'utilisateur {username} n'existe pas dans la file d'attente.")
        return redirect(url_for('admin'))
    return redirect(url_for('login'))



@administrator.route('/delete_lesson/<int:id>', methods=['POST'])
def delete_lesson(id):
    # Trouver la leçon par son ID
    lesson_to_delete = Cour.query.get_or_404(id)
    try:
        try:
            os.remove(lesson_to_delete.mainChemin)
            create_backup_zip(lesson_to_delete.mainChemin, '/backup/lessons/')
        except Exception as e:
            print(e + " pas de fichier de cour a suprimer")
        # Supprimer la leçon de la base de données
        db.session.delete(lesson_to_delete)
        db.session.commit()
        return redirect(url_for('admin.all_lessons'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression de la leçon: {str(e)}', 'error')
        return redirect(url_for('admin.all_lessons'))