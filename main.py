from src.main_chat.chatbot_manager import ChatbotManager
from src.main_chat.response_continuation import initialize_db_with_continue_statements


def main():
    # to be run one at first use of this functionality to initialize database
    initialize_db_with_continue_statements()

    chatbot_manager = ChatbotManager(intro_chatbot='Bolek', university_chatbot='Lolek',
                                     connection_uri='mongodb://localhost:27017/', database_name='PepperChatDB')
    while True:
        user_input = input('>>>')
        res = chatbot_manager.ask_chatbot(user_input)
        print('Answer = ', res)


if __name__ == '__main__':
    main()
