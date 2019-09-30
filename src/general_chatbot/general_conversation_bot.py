from chatterbot import ChatBot


def initialize_chatbot():
    return ChatBot(
        'greetings_bot',
        logic_adapters=[
            {
                'import_path': 'src.general_chatbot.logic_adapters.general_conversation_logic_adapter.GreetingAdapter',
            },
        ],
    )


class GeneralBot:
    def __init__(self):
        self.bot = initialize_chatbot()

    def get_bot_response(self, input):
        response = self.bot.get_response(input)
        return response.text


