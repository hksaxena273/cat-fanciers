from flask import Blueprint, request, jsonify
from models import db, User, Link, Rating, HiddenLink
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt

api = Blueprint('api', __name__)
jwt = JWTManager()

@api.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 409
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/links', methods=['GET'])
def get_links():
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except:
        user_id = None

    if user_id:
        hidden_links = [hidden.link_id for hidden in HiddenLink.query.filter_by(user_id=user_id)]
        links = Link.query.filter(~Link.id.in_(hidden_links)).all()
    else:
        links = Link.query.all()

    response = []
    for link in links:
        response.append({
            'id': link.id,
            'title': link.title,
            'description': link.description,
            'user': link.user.username,
            'cat_points': link.user.cat_points,
            'ratings': sum(r.value for r in link.ratings)
        })
    return jsonify(response), 200

@api.route('/link', methods=['POST'])
@jwt_required()
def add_link():
    user_id = get_jwt_identity()
    data = request.json
    new_link = Link(title=data['title'], description=data['description'], user_id=user_id)
    db.session.add(new_link)
    db.session.commit()
    return jsonify({'message': 'Link added successfully'}), 201

@api.route('/link/<int:link_id>/rate', methods=['POST'])
@jwt_required()
def rate_link(link_id):
    user_id = get_jwt_identity()
    data = request.json
    existing_rating = Rating.query.filter_by(user_id=user_id, link_id=link_id).first()
    if existing_rating:
        return jsonify({'message': 'You have already rated this link'}), 409
    new_rating = Rating(value=data['value'], user_id=user_id, link_id=link_id)
    link = Link.query.get(link_id)
    if data['value'] > 0:
        link.user.cat_points += 1
    else:
        link.user.cat_points -= 1
    db.session.add(new_rating)
    db.session.commit()
    return jsonify({'message': 'Link rated successfully'}), 201

@api.route('/link/<int:link_id>/hide', methods=['POST'])
@jwt_required()
def hide_link(link_id):
    user_id = get_jwt_identity()
    hidden_link = HiddenLink(user_id=user_id, link_id=link_id)
    db.session.add(hidden_link)
    db.session.commit()
    return jsonify({'message': 'Link hidden successfully'}), 200

@api.route('/user/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    ratings = Rating.query.filter_by(user_id=user_id, value=1).all()
    favorite_links = [rating.link for rating in ratings]
    response = []
    for link in favorite_links:
        response.append({
            'id': link.id,
            'title': link.title,
            'description': link.description,
            'user': link.user.username,
            'cat_points': link.user.cat_points,
            'ratings': sum(r.value for r in link.ratings)
        })
    return jsonify(response), 200

@api.route('/links/sort', methods=['GET'])
def sort_links():
    sort_by = request.args.get('sort_by')
    if sort_by == 'most_recent':
        links = Link.query.order_by(Link.id.desc()).all()
    elif sort_by == 'highest_rated':
        links = Link.query.all()
        links.sort(key=lambda link: sum(r.value for r in link.ratings), reverse=True)
    else:
        return jsonify({'message': 'Invalid sort option'}), 400

    response = []
    for link in links:
        response.append({
            'id': link.id,
            'title': link.title,
            'description': link.description,
            'user': link.user.username,
            'cat_points': link.user.cat_points,
            'ratings': sum(r.value for r in link.ratings)
        })
    return jsonify(response), 200
