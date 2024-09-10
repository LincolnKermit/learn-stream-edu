from flask import Flask, render_template, url_for, request, redirect
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    print("Log: Index page from"+request.remote_addr)
    return render_template('index.html')

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)