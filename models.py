from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    cat_points = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('links', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hidden = db.Column(db.Boolean, default=False)

    def get_rating(self):
        ratings = Rating.query.filter_by(link_id=self.id).all()
        if ratings:
            return sum(r.value for r in ratings) / len(ratings)
        return 0


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    link = db.relationship('Link', backref=db.backref('ratings', lazy=True))
