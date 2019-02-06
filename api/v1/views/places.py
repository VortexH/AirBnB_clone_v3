#!/usr/bin/python3
'''
Creates the view for the State object that handles all default
RESTful API actions
'''
from models.place import Place
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
import json

@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def retrieve_places(city_id):
    """Retrieves all places as json objects"""
    single_city = storage.get("City", city_id)
    if single_city is None:
        abort(404)
 
    if request.method == 'GET':
        ret_all_places = [place.to_dict() for place in single_city.places]
        return jsonify(ret_all_places)

    elif request.method == 'POST':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if json_dict.get('name') is None:
            return make_response(jsonify({"error": "Missing name"}), 400)
        if json_dict.get('user_id') is None:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        if storage.get("User", json_dict.get('user_id')) is None:
            abort(404)

        new_place = Place(**json_dict)
        new_place.city_id = single_city.id
        storage.new(new_place)
        storage.save()

        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def retrieve_single_place(place_id):
    """Retrieve a specific state based on ID"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in json_dict.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        storage.new(state)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
