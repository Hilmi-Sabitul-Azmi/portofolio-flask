from extensions import db
from datetime import datetime


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200))
    image_file = db.Column(db.String(120), default='default.jpg')
    github_link = db.Column(db.String(200))
    live_link = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    headline = db.Column(db.String(150))
    about = db.Column(db.Text)
    photo = db.Column(db.String(120), default='default-profile.jpg')
    email = db.Column(db.String(120))
    github = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50))
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(150))
    year_start = db.Column(db.String(50))
    year_end = db.Column(db.String(50))
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))