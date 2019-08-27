from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter


class NameRequestAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = SQLStorageAdapter(database_uri='sqlite:///code/db.sqlite13')

    def can_process(self, statement):
        statement_elements_set = set()
        for x in statement.text.lower().split():
            statement_elements_set.add(x)
        name_requests = self.db.filter(conversation='name_request')
        splitted_name_requests = set()
        for name_request in name_requests:
            for y in name_request.text.split(' '):
                splitted_name_requests.add(y)
        if len(statement_elements_set.intersection(splitted_name_requests)) > 0:
            return True
        return False

    def process(self, statement, additional_respones_parameters):
        import random
        from chatterbot.conversation import Statement
        name_responses = list(self.db.filter(conversation='name_response'))
        my_name = self.db.filter(conversation='my_name')
        response_text = name_responses[random.randint(0, len(name_responses) - 1)].text
        response_text += my_name.__next__().text
        selected_statement = Statement(response_text)
        selected_statement.confidence = 1
        return selected_statement
