from src.common_utils.language_utils.polish_language_utils import PolishLanguageUtils
import src.common_utils.constants as constants
import morfeusz2

from src.common_utils.database_service import DatabaseProxy

word_class_name = {'noun': set(['subst', 'depr'])
                   }


def initialize_database():
    """
        run this method just when you use this code first time to initialize database with words from file
    """
    path = "./language_utils/polish_stopwords.txt"  # in case of errors make sure path is ok, `os.getcwd()`
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
    if len(morphologic_tag.intersection(word_class_name.get(word_form))) > 0:
        return True
    return False



class SentenceFilter:
    def __init__(self):
        self.utils = PolishLanguageUtils()
        self.database = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
        self.stop_words = self.prepare_stopwords_list()  # get_stop_words_from_db()

    def is_name(self, name):
        if constants.NAME in self.utils.interprate_word(name.capitalize()):
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
        for element in analysis_result:
            try:
                morphologic_tag = element[2][2]
                lemat = element[2][1]
            except IndexError:
                print('No word class avaliable after analysis in: ``extract_lemat_and_morphologic_tag``')
            morphologic_tag_set = set(morphologic_tag.split(':'))
        return lemat, morphologic_tag_set

    def filter_stop_words(self, word):
        return word[0] not in self.stop_words

    def filter_sentence(self, sentence):
        words = list(filter(lambda y: y.lower() not in self.stop_words, sentence.split()))
        sentence_filtered = list(
                   filter(lambda x_y: filter_word_form('noun', x_y[1]),  # python3 does not support tuple unpacking, that's why
                          map(lambda z: self.extract_lemma_and_morphologic_tag(z), words)))
        return sentence_filtered


input = "Kto został nowym rektorem uczelni"
print('input: ' + input)
sentence_filtered = SentenceFilter().filter_sentence(input)
print('output: ')
for sentence in sentence_filtered:
    print("    " + sentence[0])