from flask import Flask, render_template, request, redirect, url_for, session
from extensions import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci-rahasia-anda'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portofolio.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db.init_app(app)

from models import Project, Message, Profile, Skill

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return "Halaman About"


@app.route('/portfolio')
def portfolio():
    return "Halaman Portofolio"


@app.route('/contact')
def contact():
    return "Halaman Kontak" \


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)