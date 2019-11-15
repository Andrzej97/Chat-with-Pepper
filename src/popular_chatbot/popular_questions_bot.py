from chatterbot import ChatBot


class PopularQuestionsBot:
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
                    'import_path': 'src.popular_chatbot.numbers_questions_logic_adapter'
                                   '.NumbersQuestionsAdapter',
                    'database_proxy': db_proxy
                },
                {
                    'import_path': 'src.popular_chatbot.popular_questions_logic_adapter'
                                   '.PopularQuestionsAdapter',
                    'database_proxy': db_proxy
                },
            ],
        )

    def get_bot_response(self, input):
        response = self._bot.get_response(input)
        return response