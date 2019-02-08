#!/usr/bin/python3
'''
Creates a view for the link between Place and Amenity objects
that handles all default RESTful API actions
'''
from models import storage, storage_t
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
import json


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def retrieve_amenity_objects(place_id):
    """ Function that retrieves the list of all Amenity objects of a
        place
    """
    single_place = storage.get("Place", place_id)
    if single_place is None:
        abort(404)

    if request.method == 'GET':
        amenities_dicts = [single_amenity.to_dict() for single_amenity
                           in single_place.amenities]
        return jsonify(amenities_dicts)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE', 'POST']
        )
def specific_amenity(place_id, amenity_id):
    """ Handles the DELETE and POST HTTP methods

        DELETE:
            Deletes an amenity object from the db

        POST:
            Either creates a new instance of amenity with the link to a place
            or returns an existing instance with a link to the place_id
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)

    amenities_obj_list = place.amenities
    if request.method == 'DELETE':
        for amenity_obj in amenities_obj_list:
            if amenity_obj.id == amenity_id:
                storage.delete(amenity_obj)
                if storage_t != 'db':
                    try:
                        place.amenity_ids.remove(amenity_id)
                    except:
                        pass
                storage.save()
                return make_response(jsonify({}), 200)
        abort(404)

    if request.method == 'POST':
        if amenity in amenities_obj_list:
            return make_response(jsonify(amenity.to_dict()), 200)
        if storage_t == 'db':
            place.amenities.append(amenity)
        else:
            place.amenity_ids.append(amenity.id)
        place.save()
        return make_response(jsonify(amenity.to_dict()), 201)
