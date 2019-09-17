from src.general_chatbot import bot
from src.common_utils import initialize_database
from src.common_utils.database_service import DatabaseProxy
from src.common_utils.custom_exceptions import ResponseTextByTagsNotFoundError

def main():
    initialize_database.init_database()
    bot.run_bot()
    db = DatabaseProxy()
    out1 = db.add_conversation(text="Kubica", tag1="agh", tag2="sportowiec", tag3="formuła1")
    out2 = db.add_conversation(text="Orlen", tag1="agh", tag2="sportowiec", tag3="sponsor")
    print("Newly added conversations: ", out1, " and ", out2)
    res = db.get_responses_list_by_tags(tag1="agh", tag2="sportowiec")
    print("Before update = tag1 = agh, tag2 = sportowiec, text = ", res[0], ", ", res[1])
    updated_statements = []
    try:
        updated_statements = db.update_conversation_text("Orlen jest sponsorem Kubicy", tag1="agh", tag2="sportowiec")
    except ResponseTextByTagsNotFoundError:
        print("No element found for update")
    updated = db.get_responses_list_by_tags(tag1="agh", tag2="sportowiec")
    for idx, up in enumerate(updated_statements):
        print("After update = tag1 = agh, tag2 = sportowiec, updated text = ", updated[idx], " == up = ", up)
    print()
    try:
        db.printDocumentsByTags(tag1="agh", tag2="sportowiec")
    except ResponseTextByTagsNotFoundError:
        print("Elements matching given tags not found")
    removed1 = db.remove_conversation(tag1="agh", tag2="sportowiec", tag3="formuła1")
    removed2 = db.remove_conversation(tag1="agh", tag2="sportowiec", tag3="sponsor")
    print("Removed conversations text = ", removed1, ", ", removed2)

if __name__ == '__main__':
    main()