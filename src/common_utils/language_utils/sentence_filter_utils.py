from configuration import Configuration as configuration
from src.common_utils.database.database_service import DatabaseProxy
from src.common_utils.language_utils.polish_language_utils import PolishLanguageUtils

word_class_name = {'noun': {'subst', 'depr'}
                   }


def initialize_database():
    """
        run this method just when you use this code first time to initialize database with words from file
    """
    path = "./language_utils/polish_stopwords.txt"  # in case of errors make sure that path is ok, `os.getcwd()`
    # command is useful
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    db.create_new_collection('polish_stop_words')
    result = from_txt_file_to_list(path)
    list = []
    for r in result:
        list.append({'text': r})
    db.add_many_new_docs_to_collection('polish_stop_words', list)


def from_txt_file_to_list(path):
    file = open(path, "r")
    lines = list(map(lambda x: x.rstrip(), list(file.readlines())))
    return lines


def filter_word_form(word_form, morphologic_tag):
    return len(morphologic_tag.intersection(word_class_name.get(word_form))) > 0

def delete_additional_info_after_colon(word):
    index = word.find(':')
    if index == -1:
        return word
    return word[:index]

def list_to_str_with_colons(list):
    # print('list_to_str_with_colons list param: ', list)
    string = ''
    for elem in list:
        string += elem + ':'
    string = string[:-1]
    return string

class SentenceFilter:
    def __init__(self):
        self.utils = PolishLanguageUtils()
        self.database = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
        self.stop_words = self.prepare_stopwords_list()  # get_stop_words_from_db()

    def is_name(self, name):
        if configuration.NAME.value in self.utils.interpret_word(name.capitalize()):
            return True
        return False

    def prepare_stopwords_list(self):
        result_list = []
        result = self.database.get_docs_from_collection('polish_stop_words', {"text": {'$exists': True}})
        for r in result:
            result_list.append(r["text"])
        return result_list

    def extract_lemma_and_morphological_tag(self, word):
        morphological_tag = None
        morphological_tag_set = None
        lemma = None
        analysis_result = self.utils.morfeusz.analyse(word)
        for element in analysis_result:
            try:
                morphological_tag = element[2][2]
                lemma = element[2][1]
            except IndexError:
                print('No word class available after analysis in: ``extract_lemma_and_morphologic_tag``')
            morphological_tag_set = set(morphological_tag.split(':'))
        return lemma, morphological_tag_set

    def extract_lemma(self, word, response_cont=None):
        lemmas = []
        analysis_result = self.utils.morfeusz.analyse(word)
        if len(analysis_result) == 0:
            return None
        for element in analysis_result:
            try:
                morphological_tag = element[2][2]
                if morphological_tag == "interj":
                    continue
                lemma = element[2][1]
                lemma = delete_additional_info_after_colon(lemma)
                if lemma not in lemmas:
                    lemmas.append(lemma)
            except IndexError:
                return None
        return lemmas[0] if response_cont is not None else lemmas

    def filter_stop_words(self, word):
        return word[0] not in self.stop_words

    def filter_sentence(self, sentence, forms_to_filter):
        sentence_filtered = None
        words = list(filter(lambda y: y.lower() not in self.stop_words, sentence.split(' ')))
        sentence_after_extraction = list(map(lambda z: self.extract_lemma_and_morphological_tag(z), words))
        for form in forms_to_filter:
            sentence_filtered = list(
                filter(lambda x_y: filter_word_form(form, x_y[1]),
                       # python3 does not support tuple unpacking, that's why
                       sentence_after_extraction))
        return list(map(lambda x: x[0].lower(), sentence_filtered))

    def filter_sentence_complex(self, sentence):
        sentence_filtered = None
        words = list(filter(lambda y: y.lower() not in self.stop_words, sentence.split(' ')))
        sentence_after_extraction = list(map(lambda z: self.extract_lemma(z), words))
        sentence_filtered = list(map(lambda x_list: list_to_str_with_colons(x_list), sentence_after_extraction))
        sentence_filtered = list(filter(lambda y: y.lower() not in self.stop_words, sentence_filtered))
        return sentence_filtered

    def extract_lemmas_and_filter_stopwords(self, sentence):
        words = list(filter(lambda y: y.lower() not in self.stop_words, sentence.split(' ')))
        lemmas = []
        for word in words:
            lemmas.append(self.extract_lemma(word)[0].lower())
        return list(filter(lambda x: x is not None, lemmas))

    def is_sentence_about_numbers(self, sentence):
        nums_exp_single_word_list = ['ile', 'ilu' ]
        nums_exp_compl_word_list  = ['jak', 'wiele', 'dużo', 'wielu']
        splitted_sen = sentence.split(' ')
        was_word_in_complex_list = False
        for word in splitted_sen:
            if word in nums_exp_single_word_list: return True
            elif word in nums_exp_compl_word_list and was_word_in_complex_list: return True
            elif word in nums_exp_compl_word_list: was_word_in_complex_list = True
        return False