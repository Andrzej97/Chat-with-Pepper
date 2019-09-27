from chatterbot import ChatBot

from src.common_utils.bot_context import BotContext
from src.common_utils.types_of_conversation import TypeOfOperation


# TODO: add database cleaning method

def initialize_chatbot(context):
    return ChatBot(
        'greetings_bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'src.general_chatbot.greetings_logic_adapter.GreetingAdapter',
                'conversation_context': context,

            },
            {
                'import_path': 'src.general_chatbot.name_request_logic_adapter.NameRequestAdapter',
                'conversation_context': context,

            },
            {
                'import_path': 'src.general_chatbot.basic_question_logic_adapter.BasicQuestionAdapter',
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


def run_bot():
    bot_context = BotContext()
    bot = initialize_chatbot(bot_context)

    ##### some tests
    # p: person
    # r: robot
    print("p: cześć")
    print('r: ' + get_bot_response("cześć", bot, bot_context))
    print("p: u mnie okej, a u Ciebie?")
    print('r: ' + get_bot_response("u mnie okej a u Ciebie", bot, bot_context))
    print("p: jestem Witek")
    print('r: ' + get_bot_response("mam na imię Witek", bot, bot_context))
    #
    # print("p: Gdzie jest AGH")
    # print('r: ' + get_bot_response("Gdzie jest AGH", bot, bot_context))


