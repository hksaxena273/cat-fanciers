import os
from flask import Flask
from models import db, User, Link, Rating
from routes import api
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if not User.query.first():
            user1 = User(username='user1')
            user1.set_password('password')
            user2 = User(username='user2')
            user2.set_password('password')
            user3 = User(username='user3')
            user3.set_password('password')
            
            link1 = Link(title='Cute Cat', description='A very cute cat', user=user1)
            link2 = Link(title='Funny Cat', description='A very funny cat', user=user1)
            link3 = Link(title='Cat Video', description='A hilarious cat video', user=user2)
            link4 = Link(title='Cat Meme', description='A popular cat meme', user=user2)
            link5 = Link(title='Adorable Kitten', description='An adorable kitten', user=user3)
            
            db.session.add_all([user1, user2, user3, link1, link2, link3, link4, link5])
            db.session.commit()

            rating1 = Rating(value=1, user=user1, link=link2)
            rating2 = Rating(value=-1, user=user2, link=link1)
            rating3 = Rating(value=1, user=user2, link=link3)
            rating4 = Rating(value=1, user=user3, link=link4)
            rating5 = Rating(value=1, user=user3, link=link1)
            
            db.session.add_all([rating1, rating2, rating3, rating4, rating5])
            db.session.commit()
        
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
