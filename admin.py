import os
from flask import Blueprint, flash, redirect, render_template, url_for
from py.db import db
from py.model import Homework, Cour


administrator = Blueprint('admin', __name__, template_folder='templates/admin')


@administrator.route('/all_homework')
def all_homework():
    # Récupérer tous les devoirs
    homeworks = Homework.query.all()
    return render_template('all_homework.html', homeworks=homeworks)

@administrator.route('/all_lessons')
def all_lessons():
    # Récupérer tous les devoirs
    cours = Cour.query.all()
    return render_template('all_lessons.html', lessons=cours)

@administrator.route('/delete_lesson/<int:id>', methods=['POST'])
def delete_lesson(id):
    # Trouver la leçon par son ID
    lesson_to_delete = Cour.query.get_or_404(id)
    try:
        #os.remove(lesson_to_delete.Mainchemin)
        # Supprimer la leçon de la base de données
        db.session.delete(lesson_to_delete)
        db.session.commit()
        return redirect(url_for('admin.all_lessons'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression de la leçon: {str(e)}', 'error')
        return redirect(url_for('admin.all_lessons'))