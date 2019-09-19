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


def default_response():
    return Statement(DEFAULT_RESPONSE)
