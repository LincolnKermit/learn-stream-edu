from flask import Flask, render_template, request, redirect, url_for
from day import *
from py.db import db
from py.model import Homework
from datetime import datetime, timedelta
from sys_lib_framework import loading_defined

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homework.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialiser db avec l'application Flask

@app.context_processor
def inject_functions():
    return dict(what_day_month=what_day_month)

@app.route('/admin')
def admin():
    return render_template('admin_panel.html')

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

@app.route('/all_homework')
def all_homework():
    # Récupérer tous les devoirs
    homeworks = Homework.query.all()
    return render_template('all_homework.html', homeworks=homeworks)

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

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learning_redirect')
def learning_redirect():
    return render_template('learning/learning_main.html')

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


@app.route("/learning/cpp")
def learning_cpp():
    return render_template('/learning/cpp/Cc++.html')

@app.route("/learning/cpp/Lesbases")
def learning_cpp_Lesbases():
    return render_template('/learning/cpp/Lesbases.html')

@app.route("/learning/cpp/Operateurs")
def learning_cpp_Operateurs():
    return render_template('/learning/cpp/Operateurs.html')

@app.route("/learning/cpp/Variables")
def learning_cpp_Variables():
    return render_template('/learning/cpp/TypeVariables.html')

@app.route("/learning/cpp/Structure")
def learning_cpp_Structure():
    return render_template('/learning/cpp/Structure.html')

@app.route("/learning/cpp/Pointeurs")
def learning_cpp_Pointeurs():
    return render_template('/learning/cpp/Pointeurs.html')

@app.route("/learning/cpp/Allocation_Dynamique")
def learning_cpp_Allocation_Dynamique():
    return render_template('/learning/cpp/AllocationDynamique.html')

@app.route("/learning/cpp/Exemple")
def learning_cpp_Exemple():
    return render_template('/learning/cpp/Exemple.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables dans la base de données

    app.run(debug=True)
