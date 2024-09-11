from flask import Flask, render_template, request, redirect, url_for
from db import db
from model import Homework
from datetime import datetime
from sys_lib_framework import loading_defined

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homework.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialiser db avec l'application Flask


@app.route('/admin')
def admin():
    return render_template('admin_panel.html')

@app.route('/')
@app.route('/index')
def index():
    print("Log: Index page from " + request.remote_addr)
    homeworks = Homework.query.all()
    return render_template('index.html', homeworks=homeworks)

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


@app.route("/learning/c++")
def learning_cpp():
    return render_template('/learning/c++/Cc++.html')

@app.route("/learning/c++/Lesbases")
def learning_cpp_Lesbases():
    return render_template('/learning/c++/Lesbases.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables dans la base de données
    app.run(debug=True)
