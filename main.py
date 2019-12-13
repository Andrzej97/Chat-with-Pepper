from configuration import Configuration as conf
from src.database.database.database_service import DatabaseProxy
from src.main_chat.chatbot_manager import ChatbotManager


def main():
    chatbot_manager = ChatbotManager(intro_chatbot='Bolek', university_chatbot='Lolek',
                                     database=DatabaseProxy(conf.DATABASE_ADDRESS.value, conf.DATABASE_NAME.value))
    while True:
        user_input = input('>>>')
        res = chatbot_manager.ask_chatbot(user_input)
        print('Answer = ', res)


if __name__ == '__main__':
    main()
