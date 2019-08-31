from chatterbot import ChatBot

from bot_context import BotContext


# TODO: add database cleaning method

def initialize_chatbot(context):
    return ChatBot(
        'greetings_bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///code/db.sqlite13',
        logic_adapters=[
            {
                'import_path': 'context_checking_logic_adapter.ContextAdapter',
                'conversation_context': context,
            },
            {
                'import_path': 'greetings_logic_adapter.GreetingAdapter',
                'conversation_context': context,

            },
            {
                'import_path': 'name_request_logic_adapter.NameRequestAdapter',
                'conversation_context': context,

            },
            {
                'import_path': 'basic_question_logic_adapter.BasicQuestionAdapter',
                'conversation_context': context,

            },
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Przepraszam ale nie rozumiem.',
                'maximum_similarity_threshold': 0.90
            }
        ],
    )


def get_bot_response(input, bot):
    response = bot.get_response(input)
    return response.text


bot_context = BotContext()
bot = initialize_chatbot(bot_context)

##### some tests
# p: person
# r: robot
print("p: cześć")
print('r: ' + get_bot_response("Cześć", bot))
print("p: fajnie, A u Ciebie?")
print('r: ' + get_bot_response("fajnie, A u Ciebie?", bot))
print("p: Jak się nazywasz?")
print('r: ' + get_bot_response("Jak się nazywasz?", bot))
print("p: ja nazywam się Witek")
print('r: ' + get_bot_response("ja nazywam się Witek", bot))
