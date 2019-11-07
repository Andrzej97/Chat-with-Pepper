import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.bot_context import BotContext
from src.general_chatbot.intro_conversation_bot import IntroBot
from src.main_chat.response_continuation import ResponseContinuationHandler
from src.university_chatbot.university_conversation_bot import UniversityBot


class ChatbotManager:
    def __init__(self, **kwargs):
        self._intro_chatbot_name = kwargs.get('intro_chatbot', 'Żwirek')  # our chatbots code names
        self._university_chatbot_name = kwargs.get('university_chatbot', 'Muchomorek')
        self.db = kwargs.get('database')
        bot_context = BotContext()
        self._intro_chatbot = IntroBot(self._intro_chatbot_name, bot_context, self.db)
        self._university_chatbot = UniversityBot(self._university_chatbot_name, self.db)
        self._is_intro_bot_unemployed = False
        self.response_continuation_handler = ResponseContinuationHandler(self.db)

    def _ask_intro_chatbot(self, processed_sentence):
        response = self._intro_chatbot.get_bot_response(processed_sentence)
        self._intro_chatbot.context_update(response.in_response_to)
        return response.text, response.confidence

    def _ask_university_chatbot(self, processed_sentence):
        response = self._university_chatbot.get_bot_response(processed_sentence)
        return response.text, response.confidence

    def _check_is_intro_chatbot_unemployed(self):
        if not self._is_intro_bot_unemployed:
            self._is_intro_bot_unemployed = self._intro_chatbot.check_is_bot_unemployed() \
                                            or self._university_chatbot.check_was_requested_in_row_above_thresh()
        return self._is_intro_bot_unemployed

    def check_is_intro_chatbot_part_employed(self):
        return self._intro_chatbot.check_is_bot_partially_employed()

    def ask_chatbot(self, user_input):  # this is key method which is called from main.py

        response_from_handler = self.response_continuation_handler.return_next_part_of_response(user_input)
        if response_from_handler is not None:
            return response_from_handler
        if self._check_is_intro_chatbot_unemployed():
            chatbot_response, c1 = self._ask_university_chatbot(user_input)
            print('University chatbot = ', user_input, ' c1 = ', c1)
        elif self.check_is_intro_chatbot_part_employed():
            (i_text, i_conf) = self._ask_intro_chatbot(user_input)
            (u_text, u_conf) = self._ask_university_chatbot(user_input)
            print("U_Text = {}, u_conf = {}".format(u_text, u_conf))
            conf_res = u_conf > i_conf
            self._university_chatbot.inc_responses_in_row() if conf_res \
                else self._university_chatbot.reset_responses_in_row()
            chatbot_response = u_text if conf_res else i_text
        else:
            self._university_chatbot.reset_responses_in_row()
            chatbot_response, c2 = self._ask_intro_chatbot(user_input)
            print('Intro Chatbot = ', user_input, ' c2 = ', c2)
        # self.db.add_new_doc_to_collection(configuration.RESPONSES_COLLECTION.value, response=chatbot_response)
        return statement_utils.prepare_shortened_statement(chatbot_response, 0, 1)
