from flask import jsonify
from models import User, Link, Rating

def get_link_data(link):
    return {
        'id': link.id,
        'title': link.title,
        'description': link.description,
        'user': link.user.username,
        'cat_points': link.user.cat_points,
        'created_at': link.created_at,
        'rating': link.get_rating()
    }

def get_user_data(user):
    return {
        'id': user.id,
        'username': user.username,
        'cat_points': user.cat_points
    }
