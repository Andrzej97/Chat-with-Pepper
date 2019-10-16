from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify

from src.common_utils.database_service import DatabaseProxy
import src.common_utils.constants as constants

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
        self.db = DatabaseProxy(constants.DATABASE_ADDRESS, constants.DATABASE_NAME)

    def get(self):
        result_collection = prepare_responses_list(list(self.db.collections_db[constants.RESPONSES_COLLECTION].find()))
        return result_collection


class Ping(Resource):
    def get(self):
        return jsonify("I'm Pepper and I'm ready for questions! :) ")


api.add_resource(Responses, '/responses')  # Route_1
api.add_resource(Ping, '/ping')  # Route_2

if __name__ == '__main__':
    app.run(port='5002')
