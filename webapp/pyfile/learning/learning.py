import os
import time
from flask import Blueprint, flash, redirect, render_template, session, url_for, request
from pyfile.mylib.backuper import create_backup_zip
from pyfile.db import db
from pyfile.config.model import Classe, Cour, Homework, Matiere, User
from datetime import datetime
from decoration import admin_required, student_required

learning = Blueprint('learning', __name__, template_folder='templates/admin')

# Route to display the form for adding a lesson (cour)
@learning.route('/add_lesson', methods=['GET', 'POST'])
def add_lesson():
    if request.method == 'POST':
        # Retrieve form data
        nom_cour = request.form['nomCour']
        chemin = request.form['chemin']
        id_matiere = request.form['id_matiere']

        # Create a new Cour object
        new_cour = Cour(nomCour=nom_cour, chemin=chemin, id_matiere=id_matiere)
        db.session.add(new_cour)
        db.session.commit()

        flash('Le cours a été ajouté avec succès !', 'success')
        return redirect(url_for('learning.add_lesson'))

    # Get the current user's class and associated subjects
    userClasse = Classe.query.get(session.get('id_classe'))
    matieres = Matiere.query.filter_by(id_classe=userClasse.id).all() if userClasse else []

    # Get all classes for admin to select from
    classes = Classe.query.all() if session.get('right') == 'admin' else []

    # Pass the subjects and class to the template
    return render_template('/learning/add_lesson.html', matieres=matieres, userClasse=userClasse, classes=classes)


# Route to create a new Matiere (subject)
@learning.route('/add_matiere', methods=['POST'])
def add_matiere():
    nom_matiere = request.form['nomMatiere']
    user = User.query.get(session.get('username'))

    # Set the file path for the new subject
    if user.right == 'admin':
        # Assuming a choice needs to be made, you need to send id_classe with the request
        id_classe = request.form.get('id_classe')  # Get the selected class ID from the form
        main_chemin = f'/classe/{id_classe}/{nom_matiere}'  # Use the selected class ID
    else:
        main_chemin = f'/classe/{user.id_classe}/{nom_matiere}'

    # Create a new Matiere object
    new_matiere = Matiere(nomMatiere=nom_matiere, mainChemin=main_chemin)
    db.session.add(new_matiere)
    db.session.commit()

    flash('La matière a été ajoutée avec succès !', 'success')
    return redirect(url_for('learning.add_lesson'))  # Redirect to the lesson creation page


# Routes "learning"
@learning.route('/learning_redirect')
@student_required
def learning_redirect():
    user = User.query.filter_by(username=session['username']).first()

    if user.right == 'admin':
        matieres = Matiere.query.all()  # Admin can see all subjects
    else:
        matieres = Matiere.query.filter_by(id_classe=user.id_classe).all() if user else []

    return render_template('learning/learning_main.html', matieres=matieres)
