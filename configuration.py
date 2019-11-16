from enum import Enum


class Configuration(Enum):
    NAME = 'imię'
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
    BOT_ADDRESS = 'localhost'

    # -------- MONGO COLLECTIONS NAMES -----------#
    # note: each enum name which refers to collections should contain
    # 'collection' key word - it allows for automatic collections creation, another key word is 'capped'
    RESPONSES_COLLECTION = 'responses'
    QUESTION_COLLECTION_CAPPED = 'question'
    MAIN_COLLECTION = 'main_collection'
    PHRASES_COLLECTION = 'phrases'
    POLISH_STOP_WORDS_COLLECTION = 'polish_stop_words'
    STATEMENTS_COLLECTION = 'statements'

    NUMBER_OF_SUGGESTED_RESPONSES = 5
