from app import create_app
from models import db, User, Link, Rating

app = create_app()
with app.app_context():
    db.create_all()

    # Add initial data
    user1 = User(username='user1')
    user1.set_password('password123')
    user2 = User(username='user2')
    user2.set_password('password123')
    user3 = User(username='user3')
    user3.set_password('password123')

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    link1 = Link(title='Cute Cat Video', description='A very cute cat video.', user_id=user1.id)
    link2 = Link(title='Cat Meme', description='A funny cat meme.', user_id=user2.id)
    link3 = Link(title='Cat Article', description='An article about cats.', user_id=user3.id)
    link4 = Link(title='Cat Photo', description='A beautiful cat photo.', user_id=user1.id)
    link5 = Link(title='Cat Care Tips', description='Tips for taking care of cats.', user_id=user2.id)

    db.session.add_all([link1, link2, link3, link4, link5])
    db.session.commit()

    rating1 = Rating(value=1, user_id=user1.id, link_id=link2.id)
    rating2 = Rating(value=1, user_id=user2.id, link_id=link1.id)
    rating3 = Rating(value=-1, user_id=user3.id, link_id=link4.id)

    db.session.add_all([rating1, rating2, rating3])
    db.session.commit()
