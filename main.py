from configuration import Configuration as conf
from src.database.database.database_service import DatabaseProxy
from src.main_chat.chatbot_manager import ChatbotManager


def main():
    # to be run once at first use of this functionality to initialize database

    # db = DatabaseProxy(conf.DATABASE_ADDRESS.value, conf.DATABASE_NAME.value)
    # db.update_doc_in_collection('bot_context', { }, {"context.is_during_name_processing" : True})
    # print(db.get_docs_from_collection('bot_context', { }))
    # bot = BotContext(db)
    # print(bot.get_state(key='is_during_name_processing'))
    # bot.update_state('is_during_name_processing', True)
    # print(bot.get_state(key='is_during_name_processing'))
    # db.remove_collection('bot_context')
    # db.create_new_collection('bot_context')
    # db.add_new_doc_to_collection('bot_context', context=bot_context)
    # bot_contex.get_state('')
    chatbot_manager = ChatbotManager(intro_chatbot='Bolek', university_chatbot='Lolek',
                                     database=DatabaseProxy(conf.DATABASE_ADDRESS.value, conf.DATABASE_NAME.value))
    while True:
        user_input = input('>>>')
        res = chatbot_manager.ask_chatbot(user_input)
        print('Answer = ', res)


if __name__ == '__main__':
    main()
