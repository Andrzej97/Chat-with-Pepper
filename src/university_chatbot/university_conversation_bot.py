from chatterbot import ChatBot


class UniversityBot:
    # def __init__(self):
        # self.bot = self.initialize_chatbot()

    def get_bot_response(self, input):
        response = self.bot.get_response(input)
        return response.text

    def initialize_chatbot(self, name):
        return ChatBot(
            name,
            logic_adapters=[
                {
                    'import_path': 'src.university_chatbot.university_conversation_logic_adapter'
                                   '.UniversityAdapter',
                },
            ],
        )
