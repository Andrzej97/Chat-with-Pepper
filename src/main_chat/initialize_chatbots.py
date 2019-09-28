from chatterbot import ChatBot

class ChatbotInitializer:
    def __init__(self):
        pass

    def create_general_chatbot(self, context, chatbot_name):
        return ChatBot(
            chatbot_name,
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
    # TODO: logic of this chatbot
    def create_university_chatbot(self, chatbot_name):
        return ChatBot(
            chatbot_name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter'
        )