import src.common_utils.constants as constants
from src.common_utils.database_service import DatabaseProxy
from src.common_utils.language_utils.polish_language_utils import PolishLanguageUtils
from src.common_utils.custom_exceptions import CollectionAlreadyExistsInDatabaseError

word_class_name = {'noun': set(['subst', 'depr'])
                   }


def initialize_database():
    """
        run this method just when you use this code first time to initialize database with words from file
    """
    path = "./polish_stopwords.txt"  # in case of errors make sure that path is ok, `os.getcwd()` command is useful
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    try:
        db.create_new_collection('polish_stop_words')
    except CollectionAlreadyExistsInDatabaseError:
        print('Error, error')
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

def set_to_str_with_colons(set):
    string = ''
    for elem in set:
        string += elem + ':'
    string = string[:-1]
    return string

class SentenceFilter:
    def __init__(self):
        self.utils = PolishLanguageUtils()
        self.database = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
        self.stop_words = self.prepare_stopwords_list()  # get_stop_words_from_db()

    def is_name(self, name):
        if constants.NAME in self.utils.interpret_word(name.capitalize()):
            return True
        return False

    def prepare_stopwords_list(self):
        result_list = []
        result = self.database.get_docs_from_collection('polish_stop_words', {"text": {'$exists': True}})
        for r in result:
            result_list.append(r["text"])
        return result_list

    def extract_lemma_and_morphologic_tag(self, word):
        analysis_result = self.utils.morfeusz.analyse(word)
        morphologic_tag_set = set()
        lemat = ''
        for element in analysis_result:
            try:
                morphologic_tag = element[2][2]
                lemat = element[2][1]
            except IndexError:
                print('No word class available after analysis in: ``extract_lemma_and_morphologic_tag``')
            morphologic_tag_set = set(morphologic_tag.split(':'))
        return lemat, morphologic_tag_set

    def extract_lemma(self, word):
        analysis_result = self.utils.morfeusz.analyse(word)
        for element in analysis_result:
            try:
                lemat = element[2][1]
            except IndexError:
                print('No word class available after analysis in: ``extract_lemma``')
        return lemat

    def filter_stop_words(self, word):
        return word[0] not in self.stop_words

    def filter_sentence(self, sentence, forms_to_filter):
        words = list(filter(lambda y: y.lower() not in self.stop_words, sentence.split(' ')))
        sentence_after_extraction = list(map(lambda z: self.extract_lemma_and_morphologic_tag(z), words))
        for form in forms_to_filter:
            sentence_filtered = list(
                filter(lambda x_y: filter_word_form(form, x_y[1]),
                       # python3 does not support tuple unpacking, that's why
                       sentence_after_extraction))
        return list(map(lambda x: x[0].lower(), sentence_filtered))
        raise TypeError("Argument `forms_to_filter` is not list")

    def extract_lemmas_and_filter_stopwords(self, sentence):
        words = list(filter(lambda y: y.lower() not in self.stop_words, sentence.split(' ')))
        lemmas = []
        for word in words:
            lemmas.append(self.extract_lemma(word).lower())
        return lemmas

    def andrzej_extract_lemmas_and_filter_stopwords(self, phrase):
        analysis = self.utils.morfeusz.analyse(phrase)
        tags = set([])
        old_word_index = 0
        single_tag = set([])
        # print('ANALYSIS RESULT:\n', analysis)
        for interpretation in analysis:
            # print(interpretation)
            new_word_index = interpretation[0]
            if 'interp' == interpretation[2][2]:
                continue
            if new_word_index != old_word_index:
            #     zapisz, aktualizuj index, coś jeszcze?
                if len(single_tag) > 0:
                    tags.add(set_to_str_with_colons(single_tag))
                old_word_index = new_word_index
                single_tag = set([])
            word_form = delete_additional_info_after_colon(interpretation[2][1])
            if not self.is_stopword(word_form):
                single_tag.add(word_form.lower())
            # print('INTERPRETATION: ', interpretation)
        if len(single_tag) > 0:
            tags.add(set_to_str_with_colons(single_tag))
        return tags

    def is_stopword(self, word):
        return word in self.stop_words

input = "wykształcenie, wykształcić które zdobyć można w naszej akademii, jest bardzo cenione przez pracodawców"
# # print('input: ' + input)
# sentence_filtered = SentenceFilter().filter_sentence(input, ['noun'])
# print('output: ')
# for sentence in sentence_filtered:
#     print("    " + sentence)
# #
# #
# # print(SentenceFilter().extract_lemma('wydziały'))
# print(SentenceFilter().andrzej_extract_lemmas_and_filter_stopwords(input))


