from flask import Flask, render_template, url_for, request, redirect
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)