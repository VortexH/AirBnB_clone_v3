#!/usr/bin/python3
'''
Creates the view for the State object that handles all default
RESTful API actions
'''
from models.city import City
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
import json


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_all_cities_of_state(state_id):
    """Retrieves all the cities of a specific state based on id.
    Can use get a post"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        ret_all_cities = [city.to_dict() for city in state.cities]
        return jsonify(ret_all_cities)

    elif request.method == 'POST':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if json_dict.get('name') is None:
            return make_response(jsonify({"error": "Missing name"}), 400)

        new_city = City(**json_dict)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()

        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>/', methods=['GET', 'DELETE', 'PUT'])
def get_specific_city(city_id):
    """Retrieve a specific city based on ID. Can use get, delete, and put."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in json_dict.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        storage.new(city)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
