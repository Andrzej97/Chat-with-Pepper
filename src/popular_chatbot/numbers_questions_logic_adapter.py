from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from configuration import Configuration as conf

class NumbersQuestionsAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.collection_name = conf.NUMBERS_QUEST_COLLECTION.value
        self.sentence_filter = SentenceFilter()

    def find_max_coverage(self, documents, tags):
        max_coverage = 0
        for doc in documents:
            tags_from_document = doc['tags']
            coverage = len(set(tags_from_document).intersection(set(tags)))
            max_coverage = max(max_coverage, coverage)
        return max_coverage


    def find_best_tags_response(self, documents, tags):
        max_confidence = 0
        max_id = None
        max_cov = self.find_max_coverage(documents, tags)
        for doc in documents:
            tags_from_document = doc['tags']
            coverage = len(set(tags_from_document).intersection(set(tags)))
            if coverage == max_cov:
                conf = coverage / len(doc)
                if conf > max_confidence:
                    max_confidence = conf
                    max_id = doc['_id']

        result = list(filter(lambda doc: doc['_id'] == max_id, documents))
        if len(result) > 0:
            return result[0]['text'], max_confidence
        else:
            return None


    def can_process(self, statement):
        return self.sentence_filter.is_sentence_about_numbers(statement.text)

    def process(self, statement, additional_response_selection_parameters=None):
        filtered_words = self.sentence_filter.filter_sentence(statement.text, ['noun'])
        documents_by_tags = self.db.get_docs_from_collection_by_tags_list(self.collection_name, filtered_words)
        result_text, max_conf = self.find_best_tags_response(documents_by_tags,filtered_words)
        res = Statement(result_text)
        res.confidence = 1.0
        return res


