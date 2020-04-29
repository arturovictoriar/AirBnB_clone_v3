#!/usr/bin/python3
"""RESTful API for Airbnb Clone"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def _storage(self):
    """method to handle @app.teardown_appcontext that calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a JSON-formatted 404
    status code response."""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)