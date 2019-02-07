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
def deliver_places_or_add():
    """ Route function to handle GET and POST requests

        GET returns all the places associated with a city

        POST returns a new place associated with a valid city_id and user_id

    """
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
def single_place_operations(place_id):
    """ Function to handle operations involving a single place

        Supported methods include:
        GET - returns the specific place requested

        DELETE - deletes a place object from the database and returns
                an empty dictionary to the client

        PUT - updates an instance of place with the specified key-value pairs

    """
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
        ignore_keys = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
        for key, value in json_dict.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        storage.new(place)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
