import logging

from flask import Flask
from flask_jsonpify import jsonify
from flask_restful import Resource, Api

from configuration import Configuration as configuration
from src.common_utils.database.database_service import DatabaseProxy

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
api = Api(app)

COLLECTION_NAME = 'response'


def prepare_responses_list(responses_dict):
    responses_list = []
    for doc in responses_dict:
        responses_list.append(doc[COLLECTION_NAME])
    return jsonify({'current_responses': responses_list})


class Responses(Resource):

    def __init__(self):
        self.db = DatabaseProxy(configuration.DATABASE_ADDRESS.value, configuration.DATABASE_NAME.value)

    def get(self):
        result_collection = self.db.get_elements_of_capped_collection(configuration.RESPONSES_COLLECTION.value)
        return result_collection


class Ping(Resource):
    def get(self):
        return jsonify("I'm Pepper and I'm ready for questions! :) ")


api.add_resource(Responses, '/responses')
api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run(port=configuration.REST_API_PORT.value)
