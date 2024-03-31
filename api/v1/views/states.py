#!/usr/bin/python3
"""
View for State objects that handles all
default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
@swag_from("documentaion/state/get_state.yml", methods=['GET'])
def states():
    """Method to get all the states"""
    states = storage.all(State).values()
    list_of_states = []
    for state in states:
        list_of_states.append(state.to_dict())
    return jsonify(list_of_states)


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    """Method to get a state by id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Method to delete a state by using id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def create_state():
    """Method to create a new state"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """Method to update a state"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
