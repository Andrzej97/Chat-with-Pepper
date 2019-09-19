from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter

from src.common_utils.types_of_conversation import TypeOfOperation
import src.common_utils.statement_utils as statement_utils


class BasicQuestionAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = SQLStorageAdapter(database_uri='sqlite:///resources/db.sqlite13')
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

        if len(basic_question_responses) > 0 and len(basic_question_responses_end) > 0:
            result = Statement(statement_utils.prepare_statement(
                basic_question_responses[random.randint(0, len(basic_question_responses) - 1)].text,
                basic_question_responses_end[random.randint(0, len(basic_question_responses_end) - 1)].text),
                in_response_to=TypeOfOperation.BASIC_QUESTION.value)
            result.confidence = 1
            return result
        return statement_utils.default_response()
