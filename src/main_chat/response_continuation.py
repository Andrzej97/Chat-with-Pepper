from src.common_utils.database.database_service import DatabaseProxy
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
import configuration


def initialize_db_with_continue_statements():
    # fixme: to be removed after

    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    db.add_conversation(text="powiedzieć", tag='continue')
    db.add_conversation(text="więcej", tag='continue')


class ResponseContinuationHandler:
    def __init__(self):
        self.db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
        self.offset_of_current_response

    def check_if_continuation_request(self, statement):
        continuation_requests = set(self.db.get_responses_list_by_tags(tag="continue"))
        sliced_statement = set(map(lambda x: SentenceFilter().extract_lemma(x), statement.split(' ')))
        print(self.db.get_elements_of_capped_collection(configuration.RESPONSES_COLLECTION, 0, 1))
        return len(sliced_statement.intersection(continuation_requests)) > 1


ResponseContinuationHandler().check_if_continuation_request('coś więcej')
