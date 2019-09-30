from chatterbot import ChatBot

from src.common_utils.bot_context import BotContext
from src.common_utils.types_of_conversation import TypeOfOperation


# TODO: add database cleaning method
class IntroBot:
    def __init__(self):
        self.context = BotContext()
        self.bot = self.initialize_chatbot()

    def initialize_chatbot(self):
        return ChatBot(
            'greetings_bot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=[
                {
                    'import_path': 'src.general_chatbot.logic_adapters.greetings_logic_adapter.GreetingAdapter',
                    'conversation_context': self.context,

                },
                {
                    'import_path': 'src.general_chatbot.logic_adapters.name_request_logic_adapter.NameRequestAdapter',
                    'conversation_context': self.context,

                },
                {
                    'import_path': 'src.general_chatbot.logic_adapters.basic_question_logic_adapter.BasicQuestionAdapter',
                    'conversation_context': self.context,
                },
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'Przepraszam ale nie rozumiem.',
                    'maximum_similarity_threshold': 0.40
                }
            ],
        )

    def context_update(self, type_of_conversation):
        if type_of_conversation == TypeOfOperation.NAME.value:
            self.context.is_name_request_processed = True
        if type_of_conversation == TypeOfOperation.GREETING.value:
            self.context.is_after_greeting = True
        if type_of_conversation == TypeOfOperation.NAME.value:
            self.context.is_after_introduction = True
        if type_of_conversation == TypeOfOperation.CONTEXT_NAME.value:
            self.context.is_after_name_response_reaction = True

    def get_bot_response(self, input):
        response = self.bot.get_response(input)
        self.context_update(response.in_response_to)
        return response.text

    # def prepare_bot(self):
    #     bot_context = BotContext()
    #     bot = self.initialize_chatbot(bot_context)
    #     return bot

    # def get_response(self, sentence):
    #     return self.get_bot_response(sentence)


