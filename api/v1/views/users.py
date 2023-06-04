#!/usr/bin/python3
"""new view for User object that
handles all default RESTFul API actions
"""

from flask import Blueprint, jsonify, request
from models import User

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@users_bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [user.to_dict() for user in users]
    return jsonify(users_data)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    User.delete(user)
    return jsonify({}), 200

@users_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400
    
    user = User(email=data['email'], password=data['password'])
    User.save(user)
    return jsonify(user.to_dict()), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    User.save(user)
    return jsonify(user.to_dict()), 200
