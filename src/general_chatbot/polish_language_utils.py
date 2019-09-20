def get_proper_pronoun(sentence):
    pronoun_dict = {'mój': 'twój',
                    'moje': 'twoje',
                    'mnie': 'ciebie',
                    'mam': 'ty'}

    for word in sentence.split():
        result = pronoun_dict.get(word)
        if result is not None:
            return result
    return pronoun_dict.get('mam')
