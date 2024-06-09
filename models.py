from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    cat_points = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('links', lazy=True))

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    link = db.relationship('Link', backref=db.backref('ratings', lazy=True))

class HiddenLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('hidden_links', lazy=True))
    link = db.relationship('Link', backref=db.backref('hidden_by', lazy=True))
