import operator
from functools import reduce

from chatterbot.conversation import Statement

DEFAULT_RESPONSE = "Przykro mi, nie znam odpowiedzi"


def prepare_statement(*words):
    response = ""

    if any(type(word) is list for word in words):
        words = reduce(operator.concat, words)
    for word in words:
        response += word
        response += " "
    return response


def filter_unexpected_signs(sentence):
    unexpected_signs = '[\',-'
    return ''.join(c for c in sentence if c not in unexpected_signs)


def split_to_single_words(words_set, words):
    for word in words:
        for y in word.split(' '):
            words_set.add(y)
    return words_set


def prepare_shortened_statement(many_sentence_response, first_index=0, length=1):
    if many_sentence_response is not None:
        if type(many_sentence_response) is list:
            to_split = many_sentence_response[0]
        else:
            to_split = many_sentence_response
        splitted_to_sentences = to_split.split('.')
        if first_index + length > len(splitted_to_sentences):
            return None
        return prepare_statement(splitted_to_sentences[first_index:first_index + length])
    return default_response()


def default_response():
    return Statement(DEFAULT_RESPONSE)


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


# isMatched z elifem: elif single_tag in {'agh', 'akademia'} and tag in {'agh', 'uczelnia'}: 303/346
# isMatched z elifem: elif single_tag in {'agh', 'akademia', 'uczelnia'} and tag in {'agh', 'akademia', 'uczelnia'}: 305/346
# isMatched bezz elif: 300/346
def isMatched(single_tag, set):
    for single_or_complex_tag in set:
        single_tags = extract_single_tags(single_or_complex_tag)
        for tag in single_tags:
            if single_tag == tag:
                return True
            elif single_tag in {'agh', 'akademia', 'uczelnia'} and tag in {'agh', 'akademia', 'uczelnia'}:
                return True
    return False
