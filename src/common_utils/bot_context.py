from src.common_utils.types_of_conversation import TypeOfOperation


class BotContext:
    def __init__(self):
        self.speaker_name = None
        self.is_after_greeting = False
        self.is_after_introduction = False
        self.is_name_request_processed = False
        self.is_after_name_response_reaction = False

    def context_update(self, type_of_conversation):
        if type_of_conversation == TypeOfOperation.NAME.value:
            self.is_name_request_processed = True
            self.is_after_introduction = True
        elif type_of_conversation == TypeOfOperation.GREETING.value:
            self.is_after_greeting = True
        elif type_of_conversation == TypeOfOperation.CONTEXT_NAME.value:
            self.is_after_name_response_reaction = True
