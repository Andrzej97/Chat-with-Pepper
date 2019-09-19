from stop_words import get_stop_words
import morfeusz2

name_class = {'noun': set(['subst', 'depr'])
              }

stop_words = get_stop_words('pl')

morfeusz = morfeusz2.Morfeusz()


def filter_word_form(word_form, word):
    print('a: ' + word)
    analysis_result = morfeusz.analyse(word)
    print(analysis_result)
    for element in analysis_result:
        element_class = element[2][2]
        element_class_set = set(element_class.split(':'))

        print(element_class_set.intersection(name_class.get(word_form)))
        if len(element_class_set.intersection(name_class.get(word_form))) > 0:
            return True
    return False


sentence = "Jak ma na imię dziekan AGH"
res1 = list(filter(lambda y: y not in stop_words, sentence.split()))
print(res1)
sentence_filtered = list(filter(lambda x: filter_word_form('noun', x), res1))
print(sentence_filtered)
