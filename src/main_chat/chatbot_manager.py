from src.common_utils.bot_context import BotContext
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.general_chatbot.intro_conversation_bot import IntroBot
from src.university_chatbot.university_conversation_bot import UniversityBot
from src.common_utils.database_service import DatabaseProxy


class ChatbotManager:
    def __init__(self, **kwargs):
        self._intro_chatbot_name = kwargs.get('general_chatbot', 'Żwirek')  # our chatbots code names
        self._university_chatbot_name = kwargs.get('university_chatbot', 'Muchomorek')
        db = DatabaseProxy(kwargs.get('connection_uri'), kwargs.get('database_name'))
        bot_context = BotContext()
        self._intro_chatbot = IntroBot(self._intro_chatbot_name, bot_context, db)
        self._university_chatbot = UniversityBot(self._university_chatbot_name, db)
        self._sentence_filter = SentenceFilter()
        self._is_intro_bot_unemployed = False

    def _ask_intro_chatbot(self, processed_sentence):
        response = self._intro_chatbot.get_bot_response(processed_sentence)
        self._intro_chatbot.context_update(response.in_response_to)
        return response.text

    def _ask_university_chatbot(self, processed_sentence):
        response = self._university_chatbot.get_bot_response(processed_sentence)
        return response.text

    def _check_is_intro_chatbot_unemployed(self):
        if not self._is_intro_bot_unemployed:
            self._is_intro_bot_unemployed = self._intro_chatbot.check_is_intro_chatbot_unemployed()
        return self._is_intro_bot_unemployed

    def ask_chatbot(self, user_input):  # this is key method which is called from main.py
        if self._check_is_intro_chatbot_unemployed():
            # processed_sentence = self._sentence_filter.filter_sentence(user_input, [])
            # print(processed_sentence)
            chatbot_response = self._ask_university_chatbot(user_input)
        else:
            print(user_input)
            chatbot_response = self._ask_intro_chatbot(user_input)

        return chatbot_response
