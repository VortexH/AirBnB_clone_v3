#!/usr/bin/python3
'''
Creates the view for the User object that handles all default
RESTful API actions
'''
from models.user import User
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
import json

@app_views.route('/users', methods=['GET', 'POST'])
def get_all_users():
    """Retrieves all users as json objects. Can use get and post."""
    if request.method == 'GET':
        all_users = storage.all("User")
        ret_all_users = [user.to_dict() for user in all_users.values()]
        return jsonify(ret_all_users)

    elif request.method == 'POST':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if json_dict.get('password') is None:
            return make_response(jsonify({"error": "Missing password"}), 400)

        if json_dict.get('email') is None:
            return make_response(jsonify({"error": "Missing email"}), 400)

        new_user = User(**json_dict)
        storage.new(new_user)
        storage.save()

        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def get_specific_user(user_id):
    """Retrieve a specific user based on ID. Can use get, delete, and put."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        ignore_keys = ['id','email', 'created_at', 'updated_at']
        for key, value in json_dict.items():
            if key not in ignore_keys:
                setattr(user, key, value)

        storage.new(user)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
