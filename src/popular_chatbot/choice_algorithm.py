
def complex_intersection(set1, set2):
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


# zwykly isMatched: 307/346
# isMatched z elifem: elif single_tag in {'agh', 'akademia'} and tag in {'agh', 'uczelnia'}: 308/346
def isMatched(single_tag, set):
    for single_or_complex_tag in set:
        single_tags = extract_single_tags(single_or_complex_tag)
        for tag in single_tags:
            if single_tag == tag:
                return True
            elif single_tag in {'agh', 'akademia'} and tag in {'agh', 'uczelnia'}:
                return True
    return False


def find_max_coverage(documents, tags):
    max_coverage = 0
    for doc in documents:
        tags_from_document = doc['tags']
        coverage = complex_intersection(set(tags_from_document), set(tags))
        max_coverage = max(max_coverage, coverage)
    return max_coverage


def find_best_tags_response(documents, tags):
    max_confidence = 0
    max_id = None
    max_cov = find_max_coverage(documents, tags)
    for doc in documents:
        tags_from_document = doc['tags']
        coverage = complex_intersection(set(tags_from_document), set(tags))
        if coverage == max_cov:
            tags_len_diff = len(tags) - coverage if len(tags) > coverage else 0
            conf = (coverage / len(tags_from_document)) - (tags_len_diff * 0.1)
            if conf > max_confidence:
                print('MAX_CONFIDENCE IN FIND BEST COV = ', conf, 'TAGS_FROM_DOC = ', doc['tags'], ', TEXT = ', doc['text'])
                max_confidence = conf
                max_id = doc['_id']

    result = list(filter(lambda doc: doc['_id'] == max_id, documents))
    if len(result) > 0:
        return result[0]['text'], max_confidence
    else:
        return None
