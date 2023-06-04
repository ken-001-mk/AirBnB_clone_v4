#!/usr/bin/python3

from flask import Flask
from api.v1.views.index import views
from models import storage
from os import getenv
from flasks_cors import CORS
from flask import Flask, make_response, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_storage(exception):
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Not found"}),404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}
Swagger(app)

if __name__ == "__main__":
    app.run(host, int(port), threaded=True)
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
