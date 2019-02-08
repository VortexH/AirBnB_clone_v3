#!/usr/bin/python3
"""Defines routes for displaying information about the status of the api
and a route to display counts of various models"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status_json_return():
    """ Returns a JSON file with "status": OK """

    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_count_each_class():
    """ Gets the count of each class and displays it in JSON format

        Returns:
            "Returns JSON containing each class and a count of each"
    """
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    class_count_dict = {}
    for json_display, cls_string in classes.items():
        class_count_dict[json_display] = storage.count(cls_string)

    return jsonify(class_count_dict)
