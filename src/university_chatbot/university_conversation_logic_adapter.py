from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from configuration import Configuration

class UniversityAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.sentence_filter = SentenceFilter()

    def is_accepted(self, coverage, doc_tags_length, tags):
        conf_thresh = (coverage / len(tags))
        if conf_thresh > 0:
            conf_thresh -= (1 / len(tags)) * (doc_tags_length / (doc_tags_length + 1))
        if conf_thresh >= Configuration.GOOD_ANSWER_CONFIDENCE.value:
            return conf_thresh, True
        else:
            return (0.0, False)

    def find_best_tags_coverage(self, documents, tags):
        id_of_best_cov_doc = -1
        max_conf_from_covered_docs = -1
        for document in documents:
            tags_from_document = document['tags']
            coverage = statement_utils.my_intersection(set(tags), set(tags_from_document))
            conf_thresh, was_accepted = self.is_accepted(coverage, len(set(tags_from_document)), tags)
            if was_accepted and conf_thresh >= max_conf_from_covered_docs:
                id_of_best_cov_doc = document['_id']
                max_conf_from_covered_docs = conf_thresh
        result_list = list(filter(lambda obj: obj['_id'] == id_of_best_cov_doc, documents))
        if len(result_list) > 0:
            return result_list[0]['text'], max_conf_from_covered_docs
        else:
            return None, -1

    def create_combinated_tags_list(self, single_lemmas, complex_lemmas):
        lemmas_chosen_from_complex_list = self.sentence_filter.my_generate_filtered_words_lemmas_combinations(complex_lemmas)  # list(map(lambda lemma: lemma.split(':')[0], complex_lemmas))
        tags_list = []
        tags_list.extend(single_lemmas)
        tags_list.extend(complex_lemmas)
        tags_list.extend(lemmas_chosen_from_complex_list)
        return tags_list

    def can_process(self, statement):
        return True

    def process(self, statement, additional_responses_parameters):
        tags = list(self.sentence_filter.extract_complex_lemmas_and_filter_stopwords(statement.text))
        single_lemmas, complex_lemmas = self.sentence_filter.split_to_norm_and_complex_lemmas(tags)
        if len(complex_lemmas) != 0:
            tags = self.create_combinated_tags_list(single_lemmas, complex_lemmas)

        docs_main_collection = self.db.get_docs_from_collection_by_tags_list(Configuration.MAIN_COLLECTION.value, tags)
        docs_phrases_collection = self.db.get_docs_from_collection_by_tags_list(Configuration.PHRASES_COLLECTION.value, tags)

        confidence_by_tags = 0.0
        confidence_by_lemmas = 0.0
        if len(docs_main_collection) > 0:  # matching tags exist
            result_document_tags, confidence_by_tags = self.find_best_tags_coverage(docs_main_collection, tags)
        if len(docs_phrases_collection) > 0:
            result_document_lemmas, confidence_by_lemmas = self.find_best_tags_coverage(docs_phrases_collection, tags)

        if confidence_by_lemmas >= Configuration.GOOD_ANSWER_CONFIDENCE.value \
                or confidence_by_tags >= Configuration.GOOD_ANSWER_CONFIDENCE.value:
            if confidence_by_tags >= confidence_by_lemmas:
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