from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.common_utils.language_utils.statement_utils import default_response
import src.popular_chatbot.choice_algorithm as choice_algorithm
from configuration import Configuration as config

class PopularQuestionsAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.collection_name = config.POPULAR_QUEST_COLLECTION.value
        self.sentence_filter = SentenceFilter()

    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):
        filtered_words = self.sentence_filter.filter_sentence_complex(statement.text)
        #print("FILTERED WORDS IN POPULAR BOT       = ", filtered_words)
        if len(filtered_words) == 0:
            return default_response()

        documents_by_tags = self.db.get_docs_from_collection_by_tags_list(self.collection_name, filtered_words)

        if len(documents_by_tags) == 0:
            return default_response()
        result_text, max_conf = choice_algorithm.find_best_tags_response(documents_by_tags, filtered_words)
        res = Statement(result_text)
        res.confidence = config.POP_QUEST_BOT_CONST_CONF.value if max_conf >= config.POP_QUEST_BOT_CONF_THRESH.value\
                                                               else config.DEFAULT_CONF.value

        self.db.add_new_doc_to_collection(config.RESPONSES_COLLECTION.value,
                                          confidence=res.confidence,
                                          response=res.text)
        return res