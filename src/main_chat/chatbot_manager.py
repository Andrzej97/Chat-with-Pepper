from src.common_utils.bot_context import BotContext
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.general_chatbot.intro_conversation_bot import IntroBot
from src.university_chatbot.university_conversation_bot import UniversityBot


class ChatbotManager:
    def __init__(self, **kwargs):
        self._general_chatbot_name = kwargs.get('general_chatbot', 'Żwirek')  # our chatbots code names
        self._university_chatbot_name = kwargs.get('university_chatbot', 'Muchomorek')
        self._general_chatbot = None
        self._university_chatbot = None
        self._bot_context = BotContext()
        self._sentence_filter = SentenceFilter()

    def create_chatbots(self):
        self._general_chatbot = IntroBot(self._bot_context).initialize_chatbot(self._general_chatbot_name)
        self._university_chatbot = UniversityBot.initialize_chatbot(self._university_chatbot_name)

    def _is_general_chatbot_unemployed(self):
        return self._bot_context.is_after_greeting and \
               self._bot_context.is_after_introduction and \
               self._bot_context.is_name_request_processed and \
               self._bot_context.is_after_name_response_reaction and \
               self._bot_context.speaker_name

    def _ask_general_chatbot(self, processed_sentence):
        response = self._general_chatbot.get_response(processed_sentence)
        self._bot_context.context_update(response.in_response_to)
        return response.text

    def _ask_university_chatbot(self, processed_sentence):
        response = self._university_chatbot.get_response(processed_sentence)
        return response.text

    def ask_chatbot(self, user_input):  # this is key method which is called from main.py
        if self._is_general_chatbot_unemployed():
            processed_sentence = self._sentence_filter.filter_sentence(user_input)
            print(processed_sentence)
            chatbot_response = self._ask_university_chatbot(processed_sentence)
        else:
            print(user_input)
            chatbot_response = self._ask_general_chatbot(user_input)

        return chatbot_response
