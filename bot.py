from chatterbot import ChatBot
import nltk

nltk.download('wordnet', quiet=True)


def initialize_chatbot():
    return ChatBot(
        'greetings_bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///code/db.sqlite13',
        logic_adapters=[
            {
                'import_path': 'greetings_logic_adapter.GreetingAdapter',
            },
            {
                'import_path': 'name_request_logic_adapter.NameRequestAdapter',
            },
            {
                'import_path': 'basic_question_logic_adapter.BasicQuestionAdapter',
            },
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Przepraszam ale nie rozumiem.',
                'maximum_similarity_threshold': 0.90
            }
        ]
    )


def get_bot_response(input, bot):
    response = bot.get_response(input)
    return response.text


bot = initialize_chatbot();
##### some tests
# p: person
# r: robot
print("p: cześć")
print('r: ' + get_bot_response("Cześć", bot))
print("p: fajnie, A u Ciebie?")
print('r: ' + get_bot_response("fajnie, A u Ciebie?", bot))
print("p: Jak się nazywasz?")
print('r: ' + get_bot_response("Jak się nazywasz?", bot))
