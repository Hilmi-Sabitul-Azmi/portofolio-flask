from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from extensions import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci-rahasia-anda'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portofolio.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db.init_app(app)

from models import Project, Message, Profile, Skill, Education

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    total_projects = Project.query.count()
    unread_messages = Message.query.filter_by(is_read=False).count()

    return render_template(
        'dashboard/index.html',
        total_projects=total_projects,
        unread_messages=unread_messages
    )


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


@app.route('/dashboard/projects')
def dashboard_projects():
    if 'user' not in session:
        return redirect(url_for('login'))
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('dashboard/projects.html', projects=projects)


@app.route('/dashboard/projects/add', methods=['GET', 'POST'])
def add_project():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        technologies = request.form.get('technologies')
        github_link = request.form.get('github_link')
        live_link = request.form.get('live_link')

        file = request.files.get('image')
        img_name = 'default.jpg'
        if file and file.filename != '' and allowed_file(file.filename):
            img_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))

        new_project = Project(
            title=title,
            description=description,
            technologies=technologies,
            image_file=img_name,
            github_link=github_link,
            live_link=live_link
        )
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('dashboard_projects'))
    
    return render_template('dashboard/add_project.html')


@app.route('/dashboard/projects/edit/<int:id>', methods=['Get', 'POST'])
def edit_project(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.technologies = request.form.get('technologies')
        project.github_link = request.form.get('github_link')
        project.live_link = request.form.get('live_link')

        file = request.files.get('image')
        if file and file.filename != '' and allowed_file(file.filename):
            img_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
            project.image_file = img_name

        db.session.commit()
        return redirect(url_for('dashboard_projects'))
    
    return render_template('dashboard/edit_project.html', project=project)


@app.route('/dashboard/projects/delete/<int:id>', methods=['POST'])
def delete_project(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('dashboard_projects'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)