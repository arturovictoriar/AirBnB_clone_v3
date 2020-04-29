#!/usr/bin/python3
"""
    Manage the RESTfull API for states
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def states():
    """Display all the states saved"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_state_id(state_id):
    """Display the state matched by id"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        return jsonify(state_by_id.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_state_id(state_id):
    """Delete the state matched by id"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        storage.delete(state_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_state():
    """Create a new state"""
    try:
        request.get_json()
    except:
        abort(400, {'Not a JSON'})
    if 'name' not in request.get_json():
        abort(400, {'Missing name'})
    new_state = State(**request.get_json())
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def put_state_id(state_id):
    """Update a state in database"""
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_state = storage.get('State', state_id)
    if not my_state:
        abort(404)
    for key, value in update_attr.items():
        setattr(my_state, key, value)
    storage.save()
    return my_state.to_dict()
