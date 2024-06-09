from flask import Blueprint, request, jsonify
from models import db, User, Link, Rating
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from utils import get_link_data, get_user_data

api = Blueprint('api', __name__)

@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/links', methods=['GET'])
def get_links():
    links = Link.query.filter_by(hidden=False).all()
    return jsonify([get_link_data(link) for link in links]), 200

@api.route('/links', methods=['POST'])
@jwt_required()
def add_link():
    data = request.get_json()
    user_id = get_jwt_identity()
    link = Link(title=data['title'], description=data['description'], user_id=user_id)
    db.session.add(link)
    db.session.commit()
    return jsonify(get_link_data(link)), 201

@api.route('/links/<int:link_id>/rate', methods=['POST'])
@jwt_required()
def rate_link(link_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    rating = Rating.query.filter_by(user_id=user_id, link_id=link_id).first()
    if rating:
        return jsonify({'message': 'You have already rated this link'}), 400

    link = Link.query.get_or_404(link_id)
    rating = Rating(value=data['value'], user_id=user_id, link_id=link.id)
    db.session.add(rating)
    link.user.cat_points += data['value']
    db.session.commit()
    return jsonify({'message': 'Link rated'}), 200

@api.route('/links/<int:link_id>/hide', methods=['POST'])
@jwt_required()
def hide_link(link_id):
    user_id = get_jwt_identity()
    link = Link.query.filter_by(id=link_id, user_id=user_id).first_or_404()
    link.hidden = True
    db.session.commit()
    return jsonify({'message': 'Link hidden'}), 200

@api.route('/users/<int:user_id>/favourites', methods=['GET'])
@jwt_required()
def get_favourites(user_id):
    user = User.query.get_or_404(user_id)
    ratings = Rating.query.filter_by(user_id=user_id, value=1).all()
    favourite_links = [get_link_data(r.link) for r in ratings]
    return jsonify(favourite_links), 200
