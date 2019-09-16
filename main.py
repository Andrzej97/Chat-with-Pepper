from code.general_chatbot import bot
from code.common_utils import initialize_database
from code.common_utils.database_service import DatabaseProxy

def main():
    initialize_database.init_database()
    bot.run_bot()
    db = DatabaseProxy()
    #out = db.add_conversation(text="Kubica", tag1="agh", tag2="sport")
    res = db.get_responses_list_by_tags(tag1="agh", tag2="sport")
    print("Before update = tag1 = agh, tag2 = sport, text = ", res[0])
    st_update = db.update_conversation_text("Żyła", tag1="agh", tag2="sport")
    upd = db.get_responses_list_by_tags(tag1="agh", tag2="sport")
    print("After update = tag1 = agh, tag2 = sport, text = ", upd[0], "text_update ", st_update)
    print()
    db.printDocumentsByTags(tag1="agh")

if __name__ == '__main__':
    main()