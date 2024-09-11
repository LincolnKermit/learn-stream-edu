import datetime, os
from flask import Flask, render_template, url_for, request, redirect
from sys_lib_framework import loading_defined
#from model import Homework


# n = 0
# usage : loading_defined(n)



number_visitor=number_visitor, number_blog=number_blog, number_registered=number_registered, number_premium=number_premium, logs=logs


app = Flask(__name__)


@app.route('/admin')
def admin():
    return render_template('admin_panel.html' number_visitor=number_visitor, number_blog=number_blog, number_registered=number_registered, number_premium=number_premium, logs=logs)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learning_redirect')
def learning_redirect():
    return render_template('/learning/learning_main.html')

@app.route('/add_homework', methods=['GET', 'POST'])
def add_homework():
    if request.method == 'POST':
        date_str = request.form['date']
        homework_text = request.form['homework']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        new_homework = Homework(date=date, text=homework_text)
        db.session.add(new_homework)
        db.session.commit()
        
        return redirect(url_for('index'))

    return render_template('add_homework.html')

if __name__ == '__main__':
    app.run(debug=True)