import random

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from configuration import Configuration
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.common_utils.types_of_conversation import TypeOfOperation


def parse_input(input):
    statement_elements_set = set()
    for x in input.text.lower().split():
        statement_elements_set.add(x)
    return statement_elements_set


class NameRequestAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.context = kwargs.get('conversation_context')
        self.confidence = 0
        self.robot_name_request = False
        self.name_response = False
        self.polish_sentence_tokenizer = SentenceFilter()
        self.name_requests = self.db.get_responses_list_by_tags(tag="robot_name_request")

    def can_process(self, statement):
        return self.check_if_input_contains_name_request(parse_input(statement)) \
               or self.context.get_state('is_during_name_processing')

    def process(self, statement, additional_response_selection_parameters=None):
        self.context.update_state('is_during_name_processing', True)

        response = self.prepare_response(statement)

        confidence = 0 if len(response) == 0 else 0.9

        result = Statement(statement_utils.prepare_statement(response), in_response_to=TypeOfOperation.NAME.value)
        result.confidence = confidence
        self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
                                          confidence=result.confidence,
                                          response=result.text)

        return result

    def prepare_response(self, statement):
        is_robot_introduced = self.context.get_state('is_robot_introduced')
        user_name = self.find_name(statement.text.split())
        if user_name is not None:
            self.context.update_state('is_user_introduced', True)
        is_user_introduced = self.context.get_state('is_user_introduced')

        response = []

        if self.context.get_state('is_after_name_processing') \
                and self.check_if_input_contains_name_request(
            parse_input(statement)):  # case when user ask for robot name more than once
            return self.introduce_robot()

        if is_user_introduced is False and is_robot_introduced is False:  # introduce robot and ask for user name
            self.context.update_state('is_robot_introduced', True)
            return self.introduce_robot_and_ask_for_user_name()

        if is_user_introduced is False and user_name is None:
            response.append(self.ask_for_user_name())
            self.context.update_state('is_user_introduced', True)

        if is_robot_introduced is False:
            response.append(self.introduce_robot())
            self.context.update_state('is_robot_introduced', True)

        if is_user_introduced is True \
                and not self.context.get_state('is_after_name_processing') \
                and user_name is not None:
            response.append(self.greet_user(user_name))

        if is_user_introduced is True and is_robot_introduced is True:
            self.context.update_state('is_after_name_processing', True)
        return response

    def check_if_input_contains_name_request(self, input):
        for name_request in self.name_requests:
            parsed_name_request = name_request.split(',')
            if len(input.intersection(set(parsed_name_request))) >= len(parsed_name_request):
                return True
        return False

    def ask_for_user_name(self):
        name_requests = self.db.get_responses_list_by_tags(tag="name_request")
        return name_requests[random.randint(0, len(name_requests) - 1)]

    def greet_user(self, user_name):
        response_greeting = self.db.get_random_response_by_tags(tag="name_response_end")
        general_conversation_intro = self.db.get_random_response_by_tags(tag="general_conversation_intro")
        if user_name is not None:
            response_greeting = response_greeting + user_name
        return response_greeting + general_conversation_intro

    def introduce_robot(self):
        robot_name = self.db.get_first_response_by_tags(tag="my_name")
        (introduction, name_request) = self.extract_introduction_statements()
        return introduction + robot_name

    def introduce_robot_and_ask_for_user_name(self):
        robot_name = self.db.get_first_response_by_tags(tag="my_name")
        (introduction, name_request) = self.extract_introduction_statements()
        return introduction + robot_name + name_request

    def extract_introduction_statements(self):
        name_responses = self.db.get_responses_list_by_tags(tag="name_response")
        if len(name_responses) > 0:
            name_responses_splitted = list()

            for name_response in name_responses:
                tmp = name_response.split(',')
                if len(tmp) == 2:
                    (request1, request2) = tmp
                    name_responses_splitted.append((request1, request2))

            return name_responses_splitted[random.randint(0, len(name_responses) - 1)]

    def find_name(self, sentence):
        for word in sentence:
            if self.polish_sentence_tokenizer.is_name(word):
                return word
        return None
