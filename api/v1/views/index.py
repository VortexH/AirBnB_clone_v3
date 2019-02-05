#!/usr/bin/python3
""" Contains routes for app_views """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status_json_return():
    """ Returns a JSON file with "status": OK """

    return jsonify({"status": "OK"})
