from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
import random

def my_intersection(set1, set2):
    matched = 0
    for single_or_complex_tag in set1:
        single_tags = extract_single_tags(single_or_complex_tag)
        for single_tag in single_tags:
            if isMatched(single_tag, set2):
                matched += 1
                break
    return matched

def extract_single_tags(single_or_complex_tag):
    return single_or_complex_tag.split(':')

# zwykly isMatched: 307/346
# isMatched z elifem: elif single_tag in {'agh', 'akademia'} and tag in {'agh', 'uczelnia'}: 309/346
def isMatched(single_tag, set):
    for single_or_complex_tag in set:
        single_tags = extract_single_tags(single_or_complex_tag)
        for tag in single_tags:
            if single_tag == tag:
                return True
            elif single_tag in {'agh', 'akademia'} and tag in {'agh', 'uczelnia'}:
                return True
    return False

class UniversityAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.sentence_filter = SentenceFilter()

    def find_max_coverage(self, documents, tags):
        max_coverage = 0
        for doc in documents:
            tags_from_document = doc['tags']
            coverage = len(set(tags_from_document).intersection(set(tags)))
            max_coverage = max(max_coverage, coverage)
        return max_coverage

    def is_accepted(self, coverage, doc_tags_length, tags):
        # conf_thresh = (coverage / doc_tags_length) * (1 - 1/(3*len(tags)))
        conf_thresh = (coverage / len(tags))
        # print('conf_thresh = ', conf_thresh)
        if conf_thresh > 0:
            # conf_thresh -= (doc_tags_length + len(tags) - 1) / (doc_tags_length + len(tags))
            conf_thresh -= (1 / len(tags)) * (doc_tags_length / (doc_tags_length + 1))
        # print('conf_thresh = ', conf_thresh)
        # print('coverage = ', coverage)
        # print('doc_tags_length = ', doc_tags_length)
        # print('tags = ', tags)
        # print('len(tags) = ', len(tags))
        GOOD_ANSWER_CONFIDENCE = 0.1
        if conf_thresh >= GOOD_ANSWER_CONFIDENCE:
            return conf_thresh, True
        else:
            RANDOM_CONF_THRESHOLD = 0.2
            return (conf_thresh, True) if random.uniform(0, 1) > RANDOM_CONF_THRESHOLD else (0.0, False)


    def find_best_tags_coverage(self, documents, normal_and_complex_tags):
        id_of_best_cov_doc = -1
        # print('find_best_tags_coverage:\tnormal_and_complex_tags:\t', normal_and_complex_tags)
        max_conf_from_covered_docs = 0
        was_one_selected = False
        max_coverage = -1
        tags = normal_and_complex_tags
        for document in documents:
            tags_from_document = document['tags']
            # print('tags:\t\t\t ', tags)
            # print('document[text]:\t', document['text'])
            # print('tags_from_document:\t', tags_from_document)


            # coverage = len(set(tags_from_document).intersection(set(tags)))
            coverage = my_intersection(set(tags), set(tags_from_document))

            # print('coverage: ', coverage)
            conf_thresh, was_accepted = self.is_accepted(coverage, len(set(tags_from_document)), tags)
            # print('conf_thresh: ', conf_thresh)
            if not was_one_selected:
                max_conf_from_covered_docs = conf_thresh
                id_of_best_cov_doc = document['_id']
                was_one_selected = True
                max_coverage = coverage

            if coverage >= max_coverage:
                max_coverage = coverage
                # print('tags:\t\t\t ', tags)
                # print('document[text]:\t', document['text'])
                # print('tags_from_document:\t', tags_from_document)
                # print('coverage: ', coverage)

            if was_accepted and conf_thresh >= max_conf_from_covered_docs:
                id_of_best_cov_doc = document['_id']
                max_conf_from_covered_docs = conf_thresh
                # print("Max_coverage: tags:", tags_from_document, ", len:", coverage, ", max_conf:", max_conf_from_covered_docs, ", tags:", tags)

        result_list = list(filter(lambda obj: obj['_id'] == id_of_best_cov_doc, documents))
        if len(result_list) > 0:
            return result_list[0]['text'], max_conf_from_covered_docs
        else:
            return None

    def create_tags_combinations_dict(self, normal_lemmas, complex_lemmas):
        tags_combinations = {}
        lemmas_chosen_from_complex_list = self.sentence_filter.generate_filtered_words_lemmas_combinations(complex_lemmas)  # list(map(lambda lemma: lemma.split(':')[0], complex_lemmas))
        for l in lemmas_chosen_from_complex_list:
            n_lemmas_copy = list(normal_lemmas)
            n_lemmas_copy.extend(lemmas_chosen_from_complex_list[l])
            tags_combinations[l] = n_lemmas_copy

        return tags_combinations

    def can_process(self, statement):
        return True

    def delete_additional_info_after_colon(self, word):
        index = word.find(':')
        if index == -1:
            return word
        return word[:index]

    def set_to_str_with_colons(self, set):
        string = ''
        for elem in set:
            string += elem + ':'
        string = string[:-1]
        return string

    def process(self, statement, additional_responses_parameters):
        noun_tags = self.sentence_filter.extract_complex_lemmas_and_filter_stopwords(statement.text)
        noun_tags = list(noun_tags)
        print("university_conversation_logic_adapter.py\tprocess1\tTAGS FROM SENTENCE FILTER QUESTION = \t", noun_tags)
        normal_lemmas, complex_lemmas = self.sentence_filter.split_to_norm_and_complex_lemmas(noun_tags)
        print("university_conversation_logic_adapter.py\tprocess2a\tNORMAL LEMMAS = \t", normal_lemmas)
        print("university_conversation_logic_adapter.py\tprocess2b\tCOMPLEX LEMMAS = \t", complex_lemmas)
        docs_by_tags = []
        docs_by_lemmas = []
        tags_combinations_dict = {}
        if len(complex_lemmas) != 0:
            tags_combinations_dict.update(self.create_tags_combinations_dict(normal_lemmas, complex_lemmas))
            for tags in tags_combinations_dict.values():
                tag_docs = self.db.get_docs_from_collection_by_tags_list('MAIN_COLLECTION', tags)
                lemma_docs = self.db.get_docs_from_collection_by_tags_list('PHRASES', tags)
                if tag_docs: docs_by_tags.extend(tag_docs)
                if lemma_docs: docs_by_lemmas.extend(lemma_docs)
        else:
            tags_combinations_dict[0] = noun_tags
            tag_docs = self.db.get_docs_from_collection_by_tags_list('MAIN_COLLECTION', noun_tags)
            lemma_docs = self.db.get_docs_from_collection_by_tags_list('PHRASES', noun_tags)
            if tag_docs:
                docs_by_tags.extend(tag_docs)
            if lemma_docs:
                docs_by_lemmas.extend(lemma_docs)

        confidence_by_tags = -1
        confidence_by_lemmas = -1
        # print('university_conversation_logic_adapter.py\tprocess3\tlen(docs_by_tags):\t', len(docs_by_tags))
        if len(docs_by_tags) > 0:  # matching tags exist
            result_document_tags, confidence_by_tags = self.find_best_tags_coverage(docs_by_tags, noun_tags)
            print('university_conversation_logic_adapter.py\tprocess4\tresult_codument_tags:\t', result_document_tags)
            print('university_conversation_logic_adapter.py\tprocess5\tconfidence_by_tags:\t', confidence_by_tags)
        #docs_by_lemmas = self.db.get_docs_from_collection_by_tags_list('PHRASES', noun_tags)
        # print('university_conversation_logic_adapter.py\tprocess6\tlen(docs_by_lemmas):\t', len(docs_by_lemmas))
        if len(docs_by_lemmas) > 0:
            # print("university_conversation_logic_adapter.py\tprocess7\tSEARCHING IN PHRASES STARTED")
            result_document_lemmas, confidence_by_lemmas = self.find_best_tags_coverage(docs_by_lemmas, noun_tags)
            print('university_conversation_logic_adapter.py\tprocess8\tresult_document_lemmas:\t', result_document_lemmas)
            print('university_conversation_logic_adapter.py\tprocess9\tconfidence_by_lemmas:\t', confidence_by_lemmas)
        if confidence_by_lemmas + confidence_by_tags > -2:
            # print('university_conversation_logic_adapter.py\tprocess10\tresult_document_tags:\t', result_document_tags)
            # print('university_conversation_logic_adapter.py\tprocess11\tresult_document_lemmas:\t', result_document_lemmas)
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