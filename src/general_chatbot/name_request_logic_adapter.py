import random

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter

from src.common_utils.types_of_conversation import TypeOfOperation


class NameRequestAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = SQLStorageAdapter(database_uri='sqlite:///resources/db.sqlite13')
        self.context = kwargs.get('conversation_context')
        self.confidence = 0;
        self.robot_name_request = False
        self.name_response = False

    def can_process(self, statement):
        statement_elements_set = set()
        for x in statement.text.lower().split():
            statement_elements_set.add(x)
        name_requests = self.db.filter(conversation='name_request')
        splitted_name_requests = set()
        for name_request in name_requests:
            for y in name_request.text.split(' '):
                splitted_name_requests.add(y)

        if len(statement_elements_set.intersection(
                splitted_name_requests)) > 1:
            if self.context.is_name_request_processed and not self.context.is_after_name_response_reaction:
                self.name_response = True
                return True
            self.confidence = 1
            self.robot_name_request = True
            return True
        if not self.context.is_after_introduction:
            self.confidence = 0.5
            return True
        if len(statement_elements_set) == 1 and self.context.is_name_request_processed \
                and not self.context.is_after_name_response_reaction:
            self.name_response = True
            return True
        return False

    def process_name_request(self, statement):
        name_responses = list(self.db.filter(conversation='name_response'))
        if len(name_responses) > 0:
            name_responses_splitted = list()

            for name_response in name_responses:
                tmp = name_response.text.split(',')
                if len(tmp) == 2:
                    (request1, request2) = tmp
                name_responses_splitted.append((request1, request2))

            my_name = self.db.filter(conversation='my_name')
            (response_text1, response_text2) = name_responses_splitted[random.randint(0, len(name_responses) - 1)]

            response_text = ""
            if not self.robot_name_request:
                response_text_buff = self.db.filter(conversation='no_introduction_message')
                response_text += response_text_buff.__next__().text

            response_text += response_text1
            response_text += my_name.__next__().text
            response_text += response_text2

            selected_statement = Statement(response_text)
            selected_statement.confidence = self.confidence
            selected_statement.in_response_to = TypeOfOperation.NAME.value
            return selected_statement
        return Statement("Nie znam odpowiedzi", 0)


    def process_name_response(self, statement):

        statement_list = statement.text.split()
        speaker_name = statement_list[len(statement_list) - 1]
        self.context.speaker_name = speaker_name

        name_conversation_end_responses = list(self.db.filter(conversation='name_response_end'))
        general_conversation_intro = list(self.db.filter(conversation='general_conversation_intro'))

        if len(name_conversation_end_responses) > 0 and len(general_conversation_intro) > 0:
            response_text = name_conversation_end_responses[
                                random.randint(0, len(name_conversation_end_responses) - 1)].text + ' '
            response_text += self.context.speaker_name + ' ,'
            response_text += general_conversation_intro[random.randint(0, len(general_conversation_intro) - 1)].text

            selected_statement = Statement(response_text)
            selected_statement.confidence = 0.4
            selected_statement.in_response_to = TypeOfOperation.CONTEXT_NAME.value

            return selected_statement
        return Statement("Nie znam odpowiedzi", 0)

    def process(self, statement, additional_respones_parameters):

        if self.name_response:
            return self.process_name_response(statement)
        else:
            return self.process_name_request(statement)
