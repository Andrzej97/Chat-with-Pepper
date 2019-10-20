import pymongo

from src.general_chatbot import intro_conversation_bot
from src.common_utils.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as exceptions
from src.main_chat.chatbot_manager import ChatbotManager


def main():

    chatbot_manager = ChatbotManager(intro_chatbot='Bolek', university_chatbot='Lolek',
                                     connection_uri='mongodb://localhost:27017/', database_name='PepperChatDB')
    while True:
        user_input = input('>>>')
        res = chatbot_manager.ask_chatbot(user_input)
        print('Answer = ', res)

    # db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    # db.create_new_collection('agh_tags')
    # db.remove_collection('agh_tags_from_response')
    # db.create_new_collection('agh_tags_from_response')
    # db.add_doc_with_tags_list('agh_tags', ['agh', 'wydział'], "Na AGH jest 20 wydziałów")
    # db.add_doc_with_tags_list('agh_tags', ['agh', 'wydział', 'najlepszy'], "Na AGH jest 20 wydziałów i jeden najlepszy")
    # db.add_doc_with_tags_list('agh_tags', ['agh'], "AGH rulez")
    #
    # db.add_doc_with_tags_list('agh_tags_from_response', ['budynek', 'kierunek', 'piękny'], "Na AGH jest 20 budynków")
    # db.add_doc_with_tags_list('agh_tags_from_response', ['budynek', 'kierunek', 'piękny', 'najlepszy'], "Na AGH jest 20 wydziałów i jeden najlepszy budynek")
    # db.add_doc_with_tags_list('agh_tags_from_response', ['budynek'], "AGH rulez budynek")

if __name__ == '__main__':
    main()
