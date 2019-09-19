import random

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter

import src.common_utils.statement_utils as statement_utils
from src.common_utils.types_of_conversation import TypeOfOperation


class GreetingAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = SQLStorageAdapter(database_uri='sqlite:///resources/db.sqlite13')
        self.context = kwargs.get('conversation_context')

    def can_process(self, statement):
        statement.text = statement.text.lower()
        words = self.db.filter(conversation='greeting')
        for w in words:
            if w.text == statement.text:
                return True
        return False

    def process(self, statement, additional_respones_parameters):

        greetings = list(self.db.filter(conversation='greeting'))
        greetings_request = list(self.db.filter(conversation='greeting_response'))
        if len(greetings_request) > 0 and len(greetings) > 0:
            result = Statement(
                statement_utils.prepare_statement(
                    greetings[random.randint(0, len(greetings) - 1)].text,
                    greetings_request[random.randint(0, len(greetings_request) - 1)].text),
                in_response_to=TypeOfOperation.GREETING.value)
            result.confidence = 1
            return result
        return statement_utils.default_response()
