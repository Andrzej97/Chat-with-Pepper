from src.general_chatbot import bot
from src.common_utils import initialize_database
from src.common_utils.database_service import DatabaseProxy
from src.common_utils.custom_exceptions import ResponseTextByTagsNotFoundError

def main():
    initialize_database.init_database()
    bot.run_bot()

if __name__ == '__main__':
    main()