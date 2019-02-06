#!/usr/bin/python3
'''
Creates the view for the State object that handles all default
RESTful API actions
'''
from models.state import State
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
import json

@app_views.route('/states', methods=['GET', 'POST'])
def get_all_states():
    """Retrieves all states as json objects"""
    if request.method == 'GET':
        all_states = storage.all("State")
        ret_all_states = [state.to_dict() for state in all_states.values()]
        return jsonify(ret_all_states)

    elif request.method == 'POST':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if json_dict.get('name') is None:
            return make_response(jsonify({"error": "Missing name"}), 400)

        new_state = State(**json_dict)
        storage.new(new_state)
        storage.save()

        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def get_specific_state(state_id):
    """Retrieve a specific state based on ID"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        storage.delete(state)
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
