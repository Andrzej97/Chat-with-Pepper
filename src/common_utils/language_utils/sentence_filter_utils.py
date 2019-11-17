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
        morphologic_tag_set = set()
        lemat = ''
        for element in analysis_result:
            try:
                morphological_tag = element[2][2]
                lemma = element[2][1]
            except IndexError:
                print('No word class available after analysis in: ``extract_lemma_and_morphologic_tag``')
            morphological_tag_set = set(morphological_tag.split(':'))
        return lemma, morphological_tag_set

    def extract_lemma(self, word):
        lemma = None
        analysis_result = self.utils.morfeusz.analyse(word)
        if len(analysis_result) == 0:
            return lemma
        for element in analysis_result:
            try:
                lemma = element[2][1]
            except IndexError:
                return None
        return lemma

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

    def extract_lemmas_and_filter_stopwords(self, sentence):
        words = list(filter(lambda y: y.lower() not in self.stop_words, sentence.split(' ')))
        lemmas = []
        for word in words:
            lemmas.append(self.extract_lemma(word).lower())
        return lemmas

    def extract_complex_lemmas_and_filter_stopwords(self, phrase):
        analysis = self.utils.morfeusz.analyse(phrase)
        tags = set([])
        old_word_index = 0
        single_tag = set([])
        #print('ANALYSIS RESULT:\n', analysis)
        for interpretation in analysis:
            #print("INTERPOLATION", interpretation)
            new_word_index = interpretation[0]
            if 'interp' == interpretation[2][2]:
                continue
            if new_word_index != old_word_index:
                #     zapisz, aktualizuj index, coś jeszcze?
                if len(single_tag) > 0:
                    single_tags_list = list(single_tag)
                    single_tags_list.sort()
                    #print('single tag before adding: ', single_tag)
                    tags.add(list_to_str_with_colons(single_tags_list))
                old_word_index = new_word_index
                single_tag = set([])
            word_form = delete_additional_info_after_colon(interpretation[2][1])
            if not self.is_stopword(word_form):
                single_tag.add(word_form.lower())
            #print('INTERPRETATION: ', interpretation)
        if len(single_tag) > 0:
            single_tags_list = list(single_tag)
            single_tags_list.sort()
            tags.add(list_to_str_with_colons(single_tags_list))
        return tags

    def is_stopword(self, word):
        return word.lower() in self.stop_words

    def split_to_norm_and_complex_lemmas(self, lemmas_list):
        normal_lemmas = []
        complex_lemmas = []
        for lemma in lemmas_list:
            splitted_lemmas = lemma.split(':')
            if len(splitted_lemmas) > 1 and splitted_lemmas[1] not in ['s', 's1', 's2', 's3', 'v1', 'v2', 'v3']:
                complex_lemmas.append(lemma)
            elif len(splitted_lemmas) > 1:
                normal_lemmas.append(splitted_lemmas[0])
            else:
                normal_lemmas.append(lemma)
        return normal_lemmas, complex_lemmas

    def generate_filtered_words_lemmas_combinations(self, complex_lemmas_list):
        comb_idx = 0
        combinations_dict = {}

        def create_lemmas_combinations(complex_lemmas_list, start_idx):
            nonlocal comb_idx
            if len(complex_lemmas_list) == 0:  # end of recursion
                combinations_dict[comb_idx] = []
                comb_idx = comb_idx + 1
                #print("Comb_idx = ", comb_idx, ", dict = ", combinations_dict)
                return

            possibilities = complex_lemmas_list[0].split(':')
            #print("Possibilities", possibilities)
            for possibility in possibilities:
                lemmas_list_copy = list(complex_lemmas_list)
                #print("POSSIBILITY:", possibility)
                lemma_param = lemmas_list_copy[1:] if len(lemmas_list_copy) > 1 else []
                start_idx = comb_idx
                create_lemmas_combinations(lemma_param, comb_idx)

                for k in range(start_idx, comb_idx):
                    combinations_dict[k].append(possibility)
            #print("DICT:", combinations_dict)

        create_lemmas_combinations(complex_lemmas_list, 0)
        return combinations_dict

# input = "wydziały-i-podstawowe-jednostki-organizacyjne"
# # print('input: ' + input)
# sentence_filtered = SentenceFilter().filter_sentence(input, ['noun'])
# print('output: ')
# for sentence in sentence_filtered:
#     print("    " + sentence)
# #
# #
# # print(SentenceFilter().extract_lemma('wydziały'))
# print(SentenceFilter().extract_lemmas_and_filter_stopwords(input))