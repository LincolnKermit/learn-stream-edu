from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from webapp.py import db
from webapp.py.config.model import Homework
from decoration import admin_required


homework = Blueprint('homework', __name__, template_folder='templates/homework')


@homework.route('/admin/delete_homework/<int:id>', methods=['POST'])
@admin_required
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
    

@homework.route('/admin/add_homework', methods=['GET', 'POST'])
@admin_required
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
    
    return render_template('/homework/add_homework.html')



