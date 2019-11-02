from flask import Flask
from flask_jsonpify import jsonify
from flask_restful import Resource, Api

import configuration
from src.common_utils.database.database_service import DatabaseProxy

app = Flask(__name__)
api = Api(app)

COLLECTION_NAME = 'response'


def prepare_responses_list(responses_dict):
    responses_list = []
    for doc in responses_dict:
        responses_list.append(doc[COLLECTION_NAME])
    return jsonify({'current_responses': responses_list})


class Responses(Resource):

    def __init__(self):
        self.db = DatabaseProxy(configuration.DATABASE_ADDRESS, configuration.DATABASE_NAME)

    def get(self):
        result_collection = self.db.get_elements_of_capped_collection(configuration.RESPONSES_COLLECTION)
        return result_collection


class Ping(Resource):
    def get(self):
        return jsonify("I'm Pepper and I'm ready for questions! :) ")


api.add_resource(Responses, '/responses')
api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run(port=configuration.REST_API_PORT)
