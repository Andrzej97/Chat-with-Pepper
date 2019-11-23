from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from configuration import Configuration

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
            coverage = my_intersection(set(tags), set(tags_from_document))
            conf_thresh, was_accepted = self.is_accepted(coverage, len(set(tags_from_document)), tags)
            if was_accepted and conf_thresh >= max_conf_from_covered_docs:
                id_of_best_cov_doc = document['_id']
                max_conf_from_covered_docs = conf_thresh
        result_list = list(filter(lambda obj: obj['_id'] == id_of_best_cov_doc, documents))
        if len(result_list) > 0:
            return result_list[0]['text'], max_conf_from_covered_docs
        else:
            return None, -1

    def create_combinated_tags_list(self, normal_lemmas, complex_lemmas):
        lemmas_chosen_from_complex_list = self.sentence_filter.my_generate_filtered_words_lemmas_combinations(complex_lemmas)  # list(map(lambda lemma: lemma.split(':')[0], complex_lemmas))
        tags_list = []
        tags_list.extend(normal_lemmas)
        tags_list.extend(complex_lemmas)
        tags_list.extend(lemmas_chosen_from_complex_list)
        return tags_list

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
        tags = self.sentence_filter.extract_complex_lemmas_and_filter_stopwords(statement.text)
        tags = list(tags)
        print("university_conversation_logic_adapter.py\tprocess1\tTAGS FROM SENTENCE FILTER QUESTION = \t", tags)
        normal_lemmas, complex_lemmas = self.sentence_filter.split_to_norm_and_complex_lemmas(tags)
        print("university_conversation_logic_adapter.py\tprocess2a\tNORMAL LEMMAS = \t", normal_lemmas)
        print("university_conversation_logic_adapter.py\tprocess2b\tCOMPLEX LEMMAS = \t", complex_lemmas)
        docs_by_tags = []
        docs_by_lemmas = []
        tags_combinations_dict = {}
        tags = tags
        if len(complex_lemmas) != 0:
            tags = self.create_combinated_tags_list(normal_lemmas, complex_lemmas)
        tag_docs = self.db.get_docs_from_collection_by_tags_list('MAIN_COLLECTION', tags)
        lemma_docs = self.db.get_docs_from_collection_by_tags_list('PHRASES', tags)
        if tag_docs:
            docs_by_tags.extend(tag_docs)
        if lemma_docs:
            docs_by_lemmas.extend(lemma_docs)

        confidence_by_tags = -1
        confidence_by_lemmas = -1
        # print('university_conversation_logic_adapter.py\tprocess3\tlen(docs_by_tags):\t', len(docs_by_tags))
        # print('university_conversation_logic_adapter.py\tprocess3\tdocs_by_tags:\t', docs_by_tags)
        if len(docs_by_tags) > 0:  # matching tags exist
            result_document_tags, confidence_by_tags = self.find_best_tags_coverage(docs_by_tags, tags)
            print('university_conversation_logic_adapter.py\tprocess4\tresult_codument_tags:\t', result_document_tags)
            print('university_conversation_logic_adapter.py\tprocess5\tconfidence_by_tags:\t', confidence_by_tags)
        #docs_by_lemmas = self.db.get_docs_from_collection_by_tags_list('PHRASES', tags)
        # print('university_conversation_logic_adapter.py\tprocess6\tlen(docs_by_lemmas):\t', len(docs_by_lemmas))
        if len(docs_by_lemmas) > 0:
            # print("university_conversation_logic_adapter.py\tprocess7\tSEARCHING IN PHRASES STARTED")
            result_document_lemmas, confidence_by_lemmas = self.find_best_tags_coverage(docs_by_lemmas, tags)
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