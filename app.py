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
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# pdf_txt(file) -> save it into sources/test-prod/prod-courses

@app.context_processor
def inject_functions():
    """ Injecter des fonctions globales dans les templates """
    return dict(what_day_month=what_day_month)

@app.route('/admin')
def admin():
    """ Affichage du panneau d'administration """
    cours_nb = Cour.query.count()
    return render_template('admin_panel.html', cours_nb=cours_nb)

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

@app.route('/delete_homework/<int:id>', methods=['POST'])
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

@app.route('/add_homework', methods=['GET', 'POST'])
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
    
    return render_template('add_homework.html')

@app.route('/add_lessons', methods=['GET', 'POST'])
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

def install_all_lib():
    """ Fonction pour installer les bibliothèques nécessaires """
    os.system("py -m pip install datetime")
    os.system("py -m pip install threading")
    os.system("py -m pip install pypdf2")

# Exécution de l'application
if __name__ == '__main__':
    
    # Initialiser la base de données avec l'application Flask
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # threading.Thread(target=display_uc).start()
    app.run(debug=True)
