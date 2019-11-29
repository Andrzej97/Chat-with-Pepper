from src.common_utils.database.database_service import DatabaseProxy
from src.main_chat.chatbot_manager import ChatbotManager




def main():
    # to be run once at first use of this functionality to initialize database

    chatbot_manager = ChatbotManager(intro_chatbot='Bolek', university_chatbot='Lolek',
                                     database=DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB'))
    while True:
        user_input = input('>>>')
        res = chatbot_manager.ask_chatbot(user_input)
        print('Answer = ', res)




if __name__ == '__main__':
    main()
