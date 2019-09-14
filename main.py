from code.general_chatbot import bot
from code.common_utils import initialize_database
from code.common_utils.database_service import DatabaseProxy

def main():
    initialize_database.init_database()
    bot.run_bot()
    db = DatabaseProxy()
    #db.testing_create()
    out = db.add_conversation(text="Informatyka jest super", tag1="agh", tag2="informatyka")
    res = db.get_responses_list_by_tags(tag1="agh")
    print("Database Proxy testing: count = ", db.getCount(), " out = ", out, " text = ", res[0])

if __name__ == '__main__':
    main()