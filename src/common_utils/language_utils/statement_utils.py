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
        if type(many_sentence_response) is list:
            to_split = many_sentence_response[0]
        else:
            to_split = many_sentence_response
        splitted_to_sentences = to_split.split('.')
        return prepare_statement(splitted_to_sentences[:2])
    return default_response()


def default_response():
    return Statement(DEFAULT_RESPONSE)

