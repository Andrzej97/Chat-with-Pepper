def extract_keys(document, keys):
    return [document[key] for key in keys]


def parse_documents(documents, keys):
    result = []
    for document in documents:
        result.append(dict([(key, document[key]) for key in keys]))
    return result
