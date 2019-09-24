import morfeusz2


class PolishLanguageUtils:

    def __init__(self):
        self.morfeusz = morfeusz2.Morfeusz()

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

    def generate_variation(self, word):
        variations = self.morfeusz.generate(word)
        variations_truncated = set()
        for variation in variations:
            variations_truncated.add(variation[0])
        return variations_truncated

    def interpret_word(self, word):
        analysis_result = self.morfeusz.analyse(word)
        analysis_result_list = []
        for analysis in analysis_result:
            if len(analysis[2][3]) > 0:
                analysis_result_list.append(analysis[2][3][0])
        return analysis_result_list
