from enum import Enum


class Configuration(Enum):
    NAME = 'imie'

    # ----------  BOT CONFIGURATION  ------------ #
    NUMBER_OF_SENTENCES_IN_RESPONSE = 2
    REQUESTS_IN_ROW_THRESH = 5

    # ---------- PORTS AND ADDRESSES -------------#
    ROBOT_ADDRESS = '192.168.1.102'
    ROBOT_PORT = 9559
    ROBOT_SOCKET_PORT = 9999
    REST_API_PORT = 5007
    LOCALHOST = 'localhost'
    DATABASE_NAME = 'PepperChatDB'
    DATABASE_ADDRESS = 'mongodb://localhost:27017/'

    # -------- MONGO COLLECTIONS NAMES -----------#
    RESPONSES_COLLECTION = 'responses'
    NUMBERS_QUEST_COLLECTION = 'numbers_collection'
    POPULAR_QUEST_COLLECTION = 'popular_collection'

