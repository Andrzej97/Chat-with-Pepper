import configuration
import src.common_utils.language_utils.statement_utils as statement
from src.common_utils.database.database_service import DatabaseProxy
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter


def initialize_db_with_continue_statements():
    # fixme: to be removed after adding to database initialization file

    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    db.add_conversation(text="powiedzieć", tag='continue')
    db.add_conversation(text="więcej", tag='continue')
    # ------------------------------------------------------
    db.add_conversation(text="przykro mi, to wszystko co wiem", tag='cannot_say_more')
    db.add_conversation(text="to wszystko co wiem na ten temat", tag='cannot_say_more')
    db.add_conversation(text="nie wiem więcej", tag='cannot_say_more')
    db.add_conversation(text="na tę chwilę to musi wystarczyć", tag='cannot_say_more')


class ResponseContinuationHandler:
    def __init__(self):
        self.db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
        self.response_length = configuration.NUMBER_OF_SENTENCES_IN_RESPONSE
        self.current_response_offset = 0 + self.response_length

    def is_continuation_request_asked(self, statement):
        continuation_requests = set(self.db.get_responses_list_by_tags(tag="continue"))
        sliced_statement = set(map(lambda x: SentenceFilter().extract_lemma(x), statement.split(' ')))
        return len(sliced_statement.intersection(continuation_requests)) > 1

    def return_next_part_of_response(self, question):
        if not self.is_continuation_request_asked(question):
            self.current_response_offset = 0 + self.response_length
            return None
        full_response = self.db.get_elements_of_capped_collection(configuration.RESPONSES_COLLECTION, 0, 1)
        offset = self.current_response_offset
        self.current_response_offset += self.response_length
        response = statement.prepare_shortened_statement(full_response, offset, self.response_length)
        if response is None:
            return self.db.get_random_response_by_tags(tag="cannot_say_more")
        return response
