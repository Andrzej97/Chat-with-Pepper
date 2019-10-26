import configuration
from src.common_utils.database.database_service import DatabaseProxy
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter


def initialize_db_with_continue_statements():
    # fixme: to be removed after adding to database initialization file

    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    db.add_conversation(text="powiedzieć", tag='continue')
    db.add_conversation(text="więcej", tag='continue')


class ResponseContinuationHandler:
    def __init__(self):
        self.db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
        self.offset_of_current_response

    def is_continuation_request_asked(self, statement):
        continuation_requests = set(self.db.get_responses_list_by_tags(tag="continue"))
        sliced_statement = set(map(lambda x: SentenceFilter().extract_lemma(x), statement.split(' ')))
        return len(sliced_statement.intersection(continuation_requests)) > 1

    def return_next_part_of_response(self, question):
        if not self.is_continuation_request_asked(question):
            return None
        self.db.get_elements_of_capped_collection(configuration.RESPONSES_COLLECTION, 0, 1)


ResponseContinuationHandler().is_continuation_request_asked('coś więcej')
