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
        self.name_requests = self.prepare_name_requests_set()

    def can_process(self, statement):
        if self.context.get_state('is_after_name_processing') is True:
            return False

        return self.check_if_input_contains_name_request(parse_input(statement), self.name_requests) \
               or self.context.get_state('is_during_name_processing')

    def process(self, statement, additional_response_selection_parameters=None):
        is_robot_introduced = self.context.get_state('is_robot_introduced')
        is_user_introduced = self.context.get_state('is_user_introduced')
        confidence = 0.9

        self.context.update_state('is_during_name_processing', True)
        user_name = self.find_name(statement.text.split())
        response = []

        if self.context.get_state('is_after_name_processing') \
                and self.check_if_input_contains_name_request(parse_input(statement),
                                                              self.name_requests):  # case when user ask for robot name more than once
            response.append(self.introduce_robot())

        elif is_user_introduced is False and is_robot_introduced is False:
            response.append(self.introduce_robot_and_ask_for_user_name())
            self.context.update_state('is_user_introduced', True)
            self.context.update_state('is_robot_introduced', True)

        else:
            if is_user_introduced is False:
                response.append(self.ask_for_user_name())
                self.context.update_state('is_user_introduced', True)
            if is_robot_introduced is False:
                response.append(self.introduce_robot())
                self.context.update_state('is_robot_introduced', True)

            if is_user_introduced is True and not self.context.get_state('is_after_name_processing'):
                response.append(self.greet_user(user_name))

            if is_user_introduced is True and is_robot_introduced is True:
                self.context.update_state('is_after_name_processing', True)

        if len(response) == 0:
            confidence = 0
        result = Statement(statement_utils.prepare_statement(response), in_response_to=TypeOfOperation.NAME.value)
        result.confidence = confidence
        self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
                                          confidence=result.confidence,
                                          response=result.text)

        return result

    # def perform_checking(self, input, name_requests):
    #     self.check_if_input_is_name_request(input, name_requests) \
    #     or self.check_if_user_name_given(input) \
    #     or self.check_if_not_after_introduction(input) \
    #     or self.check_if_user_introduced_itself(input)
    #
    # def check_if_user_name_given(self, input):
    #     if any(self.polish_sentence_tokenizer.is_name(x) for x in input) \
    #             and self.context.is_name_request_processed \
    #             and not self.context.is_after_name_response_reaction:
    #         self.name_response = True
    #         return True
    #     return False
    #
    # def check_if_not_after_introduction(self, input):
    #     if not self.context.is_after_introduction:
    #         self.confidence = 0.5  # case when there was no introduction, robot will response with its name, and ask for speaker name
    #         return True
    #     return False
    #
    # def check_if_user_introduced_itself(self, input):
    #     if self.context.is_name_request_processed and not self.context.is_after_name_response_reaction:
    #         self.name_response = True  # case when speaker introduced himself
    #         return True
    #     return False

    def check_if_input_contains_name_request(self, input, name_requests):
        if len(input.intersection(name_requests)) > 1:
            self.confidence = 0.6
            self.robot_name_request = True  # case when speaker asked about robot name
            return True
        return False

    def prepare_name_requests_set(self):
        name_requests = self.db.get_responses_list_by_tags(tag="name_request")
        name_responses = self.db.get_responses_list_by_tags(tag="name_response")
        splitted_name_requests = set()

        splitted_name_requests = statement_utils.split_to_single_words(splitted_name_requests,
                                                                       map(lambda x: statement_utils.
                                                                           filter_unexpected_signs(x.lower(), ','),
                                                                           name_requests))
        splitted_name_requests = statement_utils.split_to_single_words(splitted_name_requests,
                                                                       map(lambda
                                                                               x: statement_utils.filter_unexpected_signs(
                                                                           x.lower(), ','), name_responses))
        return splitted_name_requests

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

    # def can_process(self, statement):
    #     statement_elements_set = set()
    #     for x in statement.text.lower().split():
    #         statement_elements_set.add(x)
    #     name_requests = self.prepeare_name_requests_set()
    #
    #     if self.is_after_name_processing:
    #         return False
    #     if self.check_if_input_is_name_request(input, name_requests):
    #         return self.perform_checking(statement_elements_set, name_requests)
    #
    # def process_name_request(self, statement):
    #     name_responses = self.db.get_responses_list_by_tags(tag="name_response")
    #     if len(name_responses) > 0:
    #         name_responses_splitted = list()
    #
    #         for name_response in name_responses:
    #             tmp = name_response.split(',')
    #             if len(tmp) == 2:
    #                 (request1, request2) = tmp
    #                 name_responses_splitted.append((request1, request2))
    #
    #         my_name = self.db.get_first_response_by_tags(tag="my_name")
    #         (response_text1, response_text2) = name_responses_splitted[random.randint(0, len(name_responses) - 1)]
    #
    #         response = []
    #         if not self.robot_name_request:
    #             response_text_buff = self.db.get_random_response_by_tags(tag="no_introduction_message")
    #             response.append(response_text_buff)
    #
    #         response.append(response_text1)
    #         response.append(my_name)
    #         if not self.robot_name_request:
    #             response.append(response_text2)
    #         result = Statement(statement_utils.prepare_statement(
    #             response),
    #             in_response_to=TypeOfOperation.NAME.value)
    #         result.confidence = 0.9
    #         self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
    #                                           confidence=result.confidence,
    #                                           response=result.text)
    #         self.robot_name_request = False
    #         return result
    #     return statement_utils.default_response()
    #
    # def process_name_response(self, statement):
    #     speaker_name = self.find_name(list(statement.text.split()))
    #     if speaker_name is None:
    #         return Statement("", in_response_to=TypeOfOperation.CONTEXT_NAME.value)
    #     if self.polish_sentence_tokenizer.is_name(speaker_name):
    #         self.context.speaker_name = speaker_name
    #
    #     name_conversation_end_responses = self.db.get_random_response_by_tags(tag="name_response_end")
    #     general_conversation_intro = self.db.get_random_response_by_tags(tag="general_conversation_intro")
    #
    #     if name_conversation_end_responses is not None and general_conversation_intro is not None:
    #         result = Statement(statement_utils.prepare_statement(
    #             name_conversation_end_responses,
    #             self.context.speaker_name,
    #             general_conversation_intro
    #         ), in_response_to=TypeOfOperation.CONTEXT_NAME.value)
    #         self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
    #                                           confidence=result.confidence,
    #                                           response=result.text)
    #         result.confidence = 0.4
    #         return result
    #     return statement_utils.default_response()
    #
    # def process(self, statement, additional_respones_parameters):
    #
    #     if self.name_response:
    #         return self.process_name_response(statement)
    #     else:
    #         return self.process_name_request(statement)
    #
    def find_name(self, sentence):
        for word in sentence:
            if self.polish_sentence_tokenizer.is_name(word):
                return word
        return None
