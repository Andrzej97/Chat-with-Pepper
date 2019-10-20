from chatterbot.conversation import Statement
from functools import reduce
import operator

DEFAULT_RESPONSE = "Przykro mi, nie znam odpowiedzi"


def prepare_statement(*words):
    response = ""

    if any(type(word) is list for word in words):
        words = reduce(operator.concat, words)
    for word in words:
        response += word
        response += " "
    return response


def split_to_single_words(words_set, words):
    for word in words:
        for y in word.split(' '):
            words_set.add(y)
    return words_set


def prepare_shortened_statement(many_sentence_response):
    if many_sentence_response is not None:
        splitted_to_sentences = many_sentence_response.split('.')
        return prepare_statement(splitted_to_sentences[:2])
    return default_response()


def default_response():
    return Statement(DEFAULT_RESPONSE)

# res = prepare_shortened_statement("One can also make use of list slicing technique to perform the particular task of getting first and last element.\
# We can use step of whole list to skip to the last element after the first element.\
# Naive method of finding is converted to a single line using this method.")
# print(res)
