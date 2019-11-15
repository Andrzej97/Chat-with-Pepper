

def find_max_coverage(documents, tags):
    max_coverage = 0
    for doc in documents:
        tags_from_document = doc['tags']
        coverage = len(set(tags_from_document).intersection(set(tags)))
        max_coverage = max(max_coverage, coverage)
    return max_coverage


def find_best_tags_response(documents, tags):
    max_confidence = 0
    max_id = None
    max_cov = find_max_coverage(documents, tags)
    for doc in documents:
        tags_from_document = doc['tags']
        coverage = len(set(tags_from_document).intersection(set(tags)))
        if coverage == max_cov:
            conf = coverage / len(doc)
            if conf > max_confidence:
                max_confidence = conf
                max_id = doc['_id']

    result = list(filter(lambda doc: doc['_id'] == max_id, documents))
    if len(result) > 0:
        return result[0]['text'], max_confidence
    else:
        return None
