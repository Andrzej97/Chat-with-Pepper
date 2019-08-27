from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter


class GreetingAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = SQLStorageAdapter(database_uri='sqlite:///code/db.sqlite13')

    def can_process(self, statement):
        statement.text = statement.text.lower()
        words = self.db.filter(conversation='greeting')
        for w in words:
            if w.text == statement.text:
                return True
        return False

    def process(self, statement, additional_respones_parameters):
        import random
        from chatterbot.conversation import Statement

        greetings = list(self.db.filter(conversation='greeting'))
        greetings_request = list(self.db.filter(conversation='greeting_response'))
        response_text = greetings[random.randint(0, len(greetings) - 1)].text + ' '
        response_text += greetings_request[random.randint(0, len(greetings_request) - 1)].text
        selected_statement = Statement(response_text)
        selected_statement.confidence = 1
        return selected_statement
