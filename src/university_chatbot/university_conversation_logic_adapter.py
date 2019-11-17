from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter


def find_best_tags_coverage(documents, tags):
    max_ratio = -1
    id_of_max_ratio_doc = -1
    tags_len = len(tags)
    for document in documents:
        tags_from_document = document['tags']
        coverage = len(set(tags_from_document).intersection(set(tags)))
        coverage_ratio = coverage / tags_len
        length_ratio = 1 - (abs(len(tags_from_document) - tags_len) /
                            len(tags_from_document))  # this variable is to enable choosing
        # document which tags are closest to searching phrase, e.g. for ['agh','wydział'] as searching phrase, and
        # (['agh','wydział'], ['agh','wydział','najlepszy']) as tags from documents, the better one is the first of them
        overall_ratio = coverage_ratio * length_ratio
        if overall_ratio > max_ratio:
            max_ratio = overall_ratio
            id_of_max_ratio_doc = document['_id']

    result_list = list(filter(lambda obj: obj['_id'] == id_of_max_ratio_doc, documents))
    if len(result_list) > 0:
        return result_list[0]['text'], max_ratio
    else:
        return None


class UniversityAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.sentence_filter = SentenceFilter()

    def can_process(self, statement):
        return True

    def process(self, statement, additional_responses_parameters):
        noun_tags = self.sentence_filter.filter_sentence(statement.text, ['noun'])
        docs_by_tags = self.db.get_docs_from_collection_by_tags_list('MAIN_COLLECTION', noun_tags)
        confidence_by_tags = -1
        confidence_by_lemmas = -1
        if len(docs_by_tags) > 0:  # matching tags exist
            find_coverage_res = find_best_tags_coverage(docs_by_tags, noun_tags)
            if find_coverage_res is not None:
                result_document_tags, confidence_by_tags = find_coverage_res
        if confidence_by_tags < 2:  # confidence of response based on tags is not enough (0 = 0%, 1 = 100%)
            extracted_lemmas = self.sentence_filter.extract_lemmas_and_filter_stopwords(statement.text)
            docs_by_lemmas = self.db.get_docs_from_collection_by_tags_list('PHRASES', extracted_lemmas)
            if len(docs_by_lemmas) > 0:
                find_coverage_res = find_best_tags_coverage(docs_by_lemmas, extracted_lemmas)
                if find_coverage_res is not None:
                    result_document_lemmas, confidence_by_lemmas = find_coverage_res
        if confidence_by_lemmas + confidence_by_tags > -2:
            if confidence_by_tags > confidence_by_lemmas:
                res = Statement(result_document_tags)
                res.confidence = confidence_by_tags
                return res
            else:
                res = Statement(result_document_lemmas)
                res.confidence = confidence_by_lemmas
                return res
        else:
            return statement_utils.default_response()

