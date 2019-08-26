from chatterbot import ChatBot


def initialize_chatbot():
    return ChatBot(
        'greetings_bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///db.sqlite3',
        logic_adapters=[
            {
                'import_path': 'greetings_logic_adapter.GreetingAdapter',
            },
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Przepraszam ale nie rozumiem.',
                'maximum_similarity_threshold': 0.90
            }
        ]
    )


def get_response(input):
    bot = initialize_chatbot()
    response = bot.get_response(input)
    return response.text
