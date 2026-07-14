from flask import Flask, render_template, request, redirect, url_for, session
from extensions import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci-rahasia-anda'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portofolio.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db.init_app(app)

from models import Project, Message, Profile, Skill, Education

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    profile = Profile.query.first()
    skills = Skill.query.all()
    educations = Education.query.all()
    return render_template('about.html', profile=profile, skills=skills, educations=educations)


@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html', projects=projects)


@app.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    profile = Profile.query.first()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_text = request.form.get('message')

        new_message = Message(name=name, email=email, message=message_text)
        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for('contact'))
    
    return render_template('contact.html', profile=profile)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin123@':
            session['user'] = username
            return redirect(url_for('dashboard_index'))
        else:
            return render_template('dashboard/login.html', error='Username atau password salah')
        
    return render_template('dashboard/login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard_index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"Selamat datang di dashboard, {session['user']}!"


@app.route('/dashboard/messages')
def dashboard_messages():
    if 'user' not in session:
        return redirect(url_for('login'))
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('dashboard/messages.html', messages=messages)


@app.route('/dashboard/messages/read/<int:id>', methods=['POST'])
def mark_message_read(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    message = Message.query.get_or_404(id)
    message.is_read =True
    db.session.commit()
    return redirect(url_for('dashboard_messages'))


@app.route('/dashboard/messages/delete/<int:id>', methods=['POST'])
def delete_message(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('dashboard_messages'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)