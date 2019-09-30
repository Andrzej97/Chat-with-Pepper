from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

from src.common_utils.database_service import DatabaseProxy
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter


class GeneralConversationAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
        self.sentence_filter = SentenceFilter()

    def can_process(self, statement):
        return True

    def process(self, statement, additional_respones_parameters):
        tags = self.sentence_filter.filter_sentence(statement.text)
        response = self.db.get_random_response_by_tags(tags)
        return Statement(text=response)
