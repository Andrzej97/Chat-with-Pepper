import morfeusz2
from stop_words import get_stop_words

word_class_name = {'noun': set(['subst', 'depr'])
                   }


def from_txt_file_to_list(path):
    file = open(path, "r")
    lines = list(map(lambda x: x.rstrip(), list(file.readlines())))
    print(lines)
    return lines


def get_stop_words_from_db():
    return set()  # set made of stop words from database


def filter_word_form(word_form, morphologic_tag):
    if len(morphologic_tag.intersection(word_class_name.get(word_form))) > 0:
        return True
    return False


class SentenceFilter:
    def __init__(self):
        self.database = []  # db connection here
        self.stop_words = get_stop_words('pl')  # get_stop_words_from_db()
        self.analyser = morfeusz2.Morfeusz()

    def extract_lemma_and_morphologic_tag(self, word):
        analysis_result = self.analyser.analyse(word)
        # print(analysis_result)
        for element in analysis_result:
            try:
                morphologic_tag = element[2][2]
                lemat = element[2][1]
            except IndexError:
                print('No word class avaliable after analysis in: ``extract_lemat_and_morphologic_tag``')
            morphologic_tag_set = set(morphologic_tag.split(':'))
        return lemat, morphologic_tag_set

    def filter_sentence(self, sentence):
        words = list(filter(lambda y: y not in self.stop_words, sentence.split()))
        # print(words)
        sentence_filtered = list(
            filter(lambda x_y: filter_word_form('noun', x_y[1]),  # python3 does not support tuple unpacking, that's why
                   map(lambda z: self.extract_lemma_and_morphologic_tag(z), words)))
        return sentence_filtered


input = "kto jest rektorem uczelni"
print('input: ' + input)
sentence_filtered = SentenceFilter().filter_sentence(input)
print('output: ')
for sentence in sentence_filtered:
    print("    "+sentence[0])
