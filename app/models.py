from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    links = db.relationship('Link', backref='user', lazy=True)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(50))
    clicks = db.Column(db.Integer, default=0)

    logs = db.relationship('Log', backref='link', lazy=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'), nullable=False)
    click_time = db.Column(db.DateTime, default=datetime.utcnow)
    shorturl = db.Column(db.String(255))
    referrer = db.Column(db.Text)
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    country_code = db.Column(db.String(10))

# Для инициализации базы данных в Flask приложении:
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
# db.init_app(app)
