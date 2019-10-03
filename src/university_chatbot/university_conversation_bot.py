from chatterbot import ChatBot


class UniversityBot:
    def __init__(self, name, db_proxy):
        self.name = name
        self._bot = self.initialize_chatbot(db_proxy)

    def get_bot(self):
        return self._bot

    def initialize_chatbot(self, db_proxy):
        return ChatBot(
            self.name,
            logic_adapters=[
                {
                    'import_path': 'src.university_chatbot.university_conversation_logic_adapter'
                                   '.UniversityAdapter',
                    'database_proxy': db_proxy
                },
            ],
        )

    def get_bot_response(self, input):
        response = self._bot.get_response(input)
        return response