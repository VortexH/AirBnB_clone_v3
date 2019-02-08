#!/usr/bin/python3
"""
Creates the flask application, configures app with some settings, adds CORS
support and defines 2 functions that handle app teardowns and errors
"""


from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources='/*', origins='0.0.0.0')


@app.teardown_appcontext
def cleanup(func):
    """ This function calls the close method in storage
        to remove the session
    """

    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Generic error handler for 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    hbnb_host = getenv("HBNB_API_HOST")
    hbnb_port = getenv("HBNB_API_PORT")
    if hbnb_host is None:
        hbnb_host = "0.0.0.0"
    app.run(host=hbnb_host, port=int(hbnb_port), threaded=True)
