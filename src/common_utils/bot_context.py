from configuration import Configuration
from src.common_utils.types_of_conversation import TypeOfOperation


class BotContext:
    def __init__(self, database):
        self.speaker_name = None
        self.is_after_greeting = False
        self.is_after_introduction = False
        self.is_name_request_processed = False
        self.is_after_name_response_reaction = False
        self.value = {
            'is_during_name_processing': False,
            'is_after_name_processing': False,
            'is_robot_introduced': False,
            'is_user_introduced': False
        }
        self.db = database

    def context_update(self, type_of_conversation):
        if type_of_conversation == TypeOfOperation.NAME.value:
            self.is_name_request_processed = True
            self.is_after_introduction = True
        elif type_of_conversation == TypeOfOperation.GREETING.value:
            self.is_after_greeting = True
        elif type_of_conversation == TypeOfOperation.CONTEXT_NAME.value:
            self.is_after_name_response_reaction = True

    def reset_context(self):
        self.db.clear_collection(Configuration.CONTEXT_COLLECTION.value)
        self.db.add_new_doc_to_collection(Configuration.CONTEXT_COLLECTION.value, context=self.value)

    def update_state(self, key, value):
        self.db.update_doc_in_collection(Configuration.CONTEXT_COLLECTION.value, {}, {"context." + key: value})

    def get_state(self, key):
        return self.db.get_docs_from_collection(Configuration.CONTEXT_COLLECTION.value, {})[0]['context'][key]
