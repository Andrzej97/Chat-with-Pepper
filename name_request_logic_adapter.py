from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter


class NameRequestAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = SQLStorageAdapter(database_uri='sqlite:///code/db.sqlite13')
        self.context = kwargs.get('conversation_context')

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
        name_responses_splitted = list()

        for name_response in name_responses:
            (request1, request2) = name_response.text.split(',')
            name_responses_splitted.append((request1, request2))

        my_name = self.db.filter(conversation='my_name')
        (response_text1, response_text2) = name_responses_splitted[random.randint(0, len(name_responses) - 1)]
        response_text = response_text1
        response_text += my_name.__next__().text
        response_text += response_text2

        selected_statement = Statement(response_text)
        selected_statement.confidence = 1

        self.context.is_name_request_processed = True

        return selected_statement
