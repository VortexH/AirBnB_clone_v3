#!/usr/bin/python3
'''
Creates the view for the Place object that handles all default
RESTful API actions
'''
from models.review import Review
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
import json


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def get_all_reviews_of_place(place_id):
    """Retrieves all the reviews of a specific place based on id.
    Can use get a post and get."""

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        ret_all_reviews = [review.to_dict() for review in place.reviews]
        return jsonify(ret_all_reviews)

    elif request.method == 'POST':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if json_dict.get('user_id') is None:
            return make_response(jsonify({"error": "Missing user_id"}), 400)

        if storage.get("User", json_dict.get('user_id')) is None:
            abort(404)

        if json_dict.get('text') is None:
            return make_response(jsonify({"error": "Missing text"}), 400)

        new_review = Review(**json_dict)
        new_review.place_id = place_id
        storage.new(new_review)
        storage.save()

        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>/', methods=['GET', 'DELETE', 'PUT'])
def get_specific_review(review_id):
    """Retrieve a specific review based on ID. Can use get, delete, and put."""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        json_dict = request.get_json()
        if json_dict is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in json_dict.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        storage.new(review)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
