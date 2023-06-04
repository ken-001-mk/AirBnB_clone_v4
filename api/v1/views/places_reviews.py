#!/usr/bin/python3
"""new view for Review object that
handles all default RESTFul API actions
"""

from flask import abort, jsonify, request
from models import Place, Review, User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    reviews = Review.get_all_by_place(place_id)
    return jsonify([review.to_dict() for review in reviews]), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)
    review.delete()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if not user_id:
        abort(400, 'Missing user_id')
    user = User.get(user_id)
    if not user:
        abort(404)
    text = data.get('text')
    if not text:
        abort(400, 'Missing text')
    review = Review(user_id=user_id, place_id=place_id, text=text)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
