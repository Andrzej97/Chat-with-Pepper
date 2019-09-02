from chatterbot import ChatBot

from bot_context import BotContext
from types_of_conversation import TypeOfOperation


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
                'maximum_similarity_threshold': 0.40
            }
        ],
    )


def context_update(context, type_of_conversation):
    if type_of_conversation == TypeOfOperation.NAME.value:
        context.is_name_request_processed = True
    if type_of_conversation == TypeOfOperation.GREETING.value:
        context.is_after_greeting = True
    if type_of_conversation == TypeOfOperation.NAME.value:
        context.is_after_introduction = True
    if type_of_conversation == TypeOfOperation.CONTEXT_NAME.value:
        context.is_after_name_response_reaction = True


def get_bot_response(input, bot, bot_context):
    response = bot.get_response(input)
    context_update(bot_context, response.in_response_to)
    return response.text


bot_context = BotContext()
bot = initialize_chatbot(bot_context)

##### some tests
# p: person
# r: robot
print("p: co robisz")
print('r: ' + get_bot_response("co robisz", bot, bot_context))
print("p: a ja Witek")
print('r: ' + get_bot_response("a ja Witek", bot, bot_context))
print("p: Co robisz?")
print('r: ' + get_bot_response("Co robisz?", bot, bot_context))
# print("p: ja nazywam się Witek")
# print('r: ' + get_bot_response("ja nazywam się Witek", bot, bot_context))
