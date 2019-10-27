from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.database_service import DatabaseProxy
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
import random

def find_max_coverage(documents, tags):
    max_coverage = 0
    for doc in documents:
        tags_from_document = doc['tags']
        coverage = len(set(tags_from_document).intersection(set(tags)))
        max_coverage = max(max_coverage, coverage)
    return max_coverage

def is_accepted(coverage, doc_tags_length):
    conf_thresh = coverage / doc_tags_length
    if conf_thresh > 0.85:
        return conf_thresh, True
    else:
        return (conf_thresh, True) if random.uniform(0, 1) > 0.20 else (0.0, False)


def find_best_tags_coverage(documents, tags):
    id_of_best_cov_doc = -1
    #tags_len = len(tags)
    max_coverage = find_max_coverage(documents, tags)
    max_conf_from_covered_docs = 0
    was_one_selected = False
    for document in documents:
        tags_from_document = document['tags']
        coverage = len(set(tags_from_document).intersection(set(tags)))
        if max_coverage == coverage:
            conf_thresh, was_accepted = is_accepted(coverage, len(set(tags_from_document)))
            if not was_one_selected:
                max_conf_from_covered_docs = conf_thresh
                id_of_best_cov_doc = document['_id']
                was_one_selected = True

            if was_accepted and conf_thresh >= max_conf_from_covered_docs:
                id_of_best_cov_doc = document['_id']
                max_conf_from_covered_docs = conf_thresh
                print("Max_coverage: tags:", tags_from_document, ", len:", coverage, ", max_conf:",max_conf_from_covered_docs, ", tags:", tags)

    result_list = list(filter(lambda obj: obj['_id'] == id_of_best_cov_doc, documents))
    if len(result_list) > 0:
        return result_list[0]['text'], max_conf_from_covered_docs
    else:
        return None
    #raise TypeError("No `text` attribute found")


class UniversityAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.sentence_filter = SentenceFilter()

    def can_process(self, statement):
        return True

    def process(self, statement, additional_responses_parameters):
        noun_tags = self.sentence_filter.extract_lemmas_and_filter_stopwords(statement.text)
        print("TAGS FROM SENTENCE FILTER = ", noun_tags)
        docs_by_tags = self.db.get_docs_from_collection_by_tags_list('MAIN_COLLECTION', noun_tags)
        confidence_by_tags = -1
        confidence_by_lemmas = -1
        if len(docs_by_tags) > 0:  # matching tags exist
            result_document_tags, confidence_by_tags = find_best_tags_coverage(docs_by_tags, noun_tags)
        if confidence_by_tags < 2:  # confidence of response based on tags is not enough (0 = 0%, 1 = 100%)
            extracted_lemmas = self.sentence_filter.extract_lemmas_and_filter_stopwords(statement.text)
            print("Extracted_lemmas:", extracted_lemmas)
            docs_by_lemmas = self.db.get_docs_from_collection_by_tags_list('PHRASES', extracted_lemmas)
            if len(docs_by_lemmas) > 0:
                print("SEARCHING IN PHRASES STARTED")
                result_document_lemmas, confidence_by_lemmas = find_best_tags_coverage(docs_by_lemmas, extracted_lemmas)
        if confidence_by_lemmas + confidence_by_tags > -2:
            if confidence_by_tags > confidence_by_lemmas:
                res = Statement(
                    statement_utils.prepare_shortened_statement(result_document_tags))
                res.confidence = 1.0
                return res
            else:
                res = Statement(
                    statement_utils.prepare_shortened_statement(result_document_lemmas))
                res.confidence = 1.0
                return res
        else:
            return statement_utils.default_response()

