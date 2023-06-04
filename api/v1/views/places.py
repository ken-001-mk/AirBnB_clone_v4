#!/usr/bin//python3
"""new view for Place objects that
handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import app, storage, State, User, City, Place, Amenity

@app.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    places = Place.filter(city_id=city_id)
    return jsonify([place.to_dict() for place in places])

@app.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    place.delete()
    return jsonify({}), 200

@app.route('/api/v1/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = User.get(data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place.create(city_id=city_id, user_id=data['user_id'], name=data['name'])
    return jsonify(place.to_dict()), 201

@app.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    search_data = request.get_json()

    states = search_data.get('states', [])
    cities = search_data.get('cities', [])
    amenities = search_data.get('amenities', [])

    if not any([states, cities, amenities]):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    place_ids = set()

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state is not None:
                for city in state.cities:
                    place_ids.update([place.id for place in city.places])

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city is not None:
                place_ids.update([place.id for place in city.places])

    if amenities:
        amenity_ids = set(amenities)
        for place_id in list(place_ids):
            place = storage.get(Place, place_id)
            if place is not None:
                place_amenity_ids = {amenity.id for amenity in place.amenities}
                if not amenity_ids.issubset(place_amenity_ids):
                    place_ids.remove(place_id)

    places = [storage.get(Place, place_id) for place_id in place_ids]
    return jsonify([place.to_dict() for place in places if place is not None])
