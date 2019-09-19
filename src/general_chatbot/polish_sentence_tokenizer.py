from src.common_utils.polish_language_utils import PolishLanguageUtils
import src.common_utils.constants as constants


class PolishSentenceTokenizer:
    def __init__(self):
        self.utils = PolishLanguageUtils()

    def is_name(self, name):
        if constants.NAME in self.utils.interprate_word(name.capitalize()):
            return True
        return False
