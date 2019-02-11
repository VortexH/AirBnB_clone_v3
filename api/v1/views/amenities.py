#!/usr/bin/python3
'''
Creates the view for the Amenity object that handles all default
RESTful API actions
'''
from models.amenity import Amenity
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
import json


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenity_create_or_post():
    """ Handles GET and POST requests for getting a list of amenities
        or creating an entirely new amenity

    """
    if request.method == 'GET':
        all_amenities = storage.all("Amenity")
        ret_all_amenities = [amenity.to_dict()
                             for amenity in all_amenities.values()]
        return jsonify(ret_all_amenities)

    elif request.method == 'POST':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if json_dict.get('name') is None:
            return make_response(jsonify({"error": "Missing name"}), 400)

        new_amenity = Amenity(**json_dict)
        storage.new(new_amenity)
        storage.save()

        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def specific_amenity_operations(amenity_id):
    """ Handles GET, DELETE, PUT on a specific amenity

        GET will return a JSON file showing the amenity

        DELETE will remove it from the database and display an empty JSON

        PUT will update a specific amenity with key-value pairs, as long
        as the tables allow that key

        Args:
            amenity_id: a uuid string assigned to an amenity


    """
    single_amenity = storage.get("Amenity", amenity_id)
    if single_amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(single_amenity.to_dict())

    elif request.method == 'DELETE':
        storage.delete(single_amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in json_dict.items():
            if key not in ignore_keys:
                setattr(single_amenity, key, value)

        storage.new(single_amenity)
        storage.save()
        return make_response(jsonify(single_amenity.to_dict()), 200)
