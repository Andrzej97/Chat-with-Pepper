from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter

from types_of_conversation import TypeOfOperation


class BasicQuestionAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = SQLStorageAdapter(database_uri='sqlite:///code/db.sqlite13')
        self.context = kwargs.get('conversation_context')

    def can_process(self, statement):
        statement_elements_set = set()
        for x in statement.text.lower().split():
            statement_elements_set.add(x)
        basic_requests = self.db.filter(conversation='basic_question_request')
        greeting_responses = self.db.filter(conversation='greeting_response')
        splitted_name_requests = set()

        for basic_request in basic_requests:
            for y in basic_request.text.split(' '):
                splitted_name_requests.add(y)
        for greeting_response in greeting_responses:
            for y in greeting_response.text.split(' '):
                splitted_name_requests.add(y)
        if len(statement_elements_set.intersection(splitted_name_requests)) > 1:
            return True
        return False

    def process(self, statement, additional_respones_parameters):
        import random
        from chatterbot.conversation import Statement
        basic_question_responses = list(self.db.filter(conversation='basic_question_response'))
        basic_question_responses_end = list(self.db.filter(conversation='basic_question_response_end'))

        response_text = basic_question_responses[random.randint(0, len(basic_question_responses) - 1)].text
        response_text += basic_question_responses_end[random.randint(0, len(basic_question_responses_end) - 1)].text
        selected_statement = Statement(response_text)
        selected_statement.confidence = 1
        selected_statement.in_response_to = TypeOfOperation.BASIC_QUESTION.value
        return selected_statement
