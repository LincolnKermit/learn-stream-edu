import threading
from flask import Flask, flash, render_template, request, redirect, url_for
from py.backuper import create_backup_zip
from py.day import *
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

#Error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# pdf_txt(file) -> save it into sources/test-prod/prod-courses

db.init_app(app)  # Initialiser db avec l'application Flask
@app.context_processor
def inject_functions():
    return dict(what_day_month=what_day_month)

@app.route('/admin')
def admin():
    cours_nb = Cour.query.count()
    return render_template('admin_panel.html', cours_nb=cours_nb)

@app.route('/')
@app.route('/index')
def index():
    today = datetime.today().date()  # Date actuelle sans l'heure
    start_of_week = today - timedelta(days=today.weekday())  # Lundi de cette semaine
    end_of_week = start_of_week + timedelta(days=6)  # Dimanche de cette semaine

    # Début et fin de la semaine prochaine
    next_week_start = end_of_week + timedelta(days=1)  # Lundi de la semaine prochaine
    next_week_end = next_week_start + timedelta(days=6)  # Dimanche de la semaine prochaine

    # Requête pour récupérer les devoirs à partir d'aujourd'hui jusqu'à la fin de la semaine prochaine
    homeworks = Homework.query.filter(Homework.date >= today, Homework.date <= next_week_end).order_by(Homework.date.asc()).all()

    return render_template('index.html', homeworks=homeworks, week=alternance_day())

@app.route('/delete_homework/<int:id>', methods=['POST'])
def delete_homework(id):
    # Trouver le devoir par son ID
    homework_to_delete = Homework.query.get_or_404(id)
    
    try:
        # Supprimer le devoir de la base de données
        db.session.delete(homework_to_delete)
        db.session.commit()
        return redirect(url_for('all_homework'))  # Rediriger vers la page avec tous les devoirs
    except:
        return 'Une erreur s\'est produite lors de la suppression du devoir.'

@app.route('/add_homework', methods=['GET', 'POST'])
def add_homework():
    if request.method == 'POST':
        date_str = request.form['date']
        homework_text = request.form['homework']
        matiere = request.form['matiere']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        new_homework = Homework(date=date, text=homework_text, matiere=matiere)
        db.session.add(new_homework)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_homework.html')


@app.route('/add_lessons', methods=['GET', 'POST'])
def add_lessons():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        date = request.form.get('date')
        nomCour = request.form.get('nomCour')
        matiere = request.form.get('matiere')
        mainChemin = request.form.get('mainChemin')
        idf = request.form.get('idf')

        # Validation de la date
        try:
            parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            print('Date invalide. Veuillez entrer une date au format AAAA-MM-JJ.', 'error')
            return render_template('/learning/add_lessons.html')

        # Vérifier que tous les champs requis sont remplis
        if not nomCour or not matiere or not mainChemin or not idf:
            print('Tous les champs sont obligatoires.', 'error')
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
            print('Le cours a été ajouté avec succès.', 'success')
        except Exception as e:
            db.session.rollback()
            print(f'Erreur lors de l\'ajout du cours: {str(e)}', 'error')

        # Redirection vers l'index
        return redirect(url_for('index'))

    # Méthode GET : affichage du formulaire
    return render_template('/learning/add_lessons.html')


@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

@app.route('/about')
def about():
    return render_template('about.html')

app.register_blueprint(learning_bp)
app.register_blueprint(administrator)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    threading.Thread(target=display_uc).start()
    app.run(debug=True)
    
