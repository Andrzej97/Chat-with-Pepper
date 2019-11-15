import src.common_utils.database_preparing.initialize_database as general_data
from src.common_utils.database_service import DatabaseProxy
import src.common_utils.database_preparing.csv_to_database_filler as scrapper_data
import src.common_utils.custom_exceptions as Exceptions


def initialize_language_utils_database(db):
    """
        run this method just when you use this code first time to initialize database with words from file
    """
    path = "./polish_stopwords.txt"  # in case of errors make sure that path is ok, `os.getcwd()` command is useful
    result = from_txt_file_to_list(path)
    list = []
    for r in result:
        list.append({'text': r})
    try:
        db.create_new_collection('polish_stop_words')
        db.add_many_new_docs_to_collection('polish_stop_words', list)
    except Exceptions.CollectionAlreadyExistsInDatabaseError:
        db.add_many_new_docs_to_collection('polish_stop_words', list)


def from_txt_file_to_list(path):
    file = open(path, "r")
    lines = list(map(lambda x: x.rstrip(), list(file.readlines())))
    return lines


def main():
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    initialize_language_utils_database(db)
    general_data.init_database(db)
    scrapper_data.initialize_main_collection_from_scrapper(db)



if __name__ == '__main__':
    main()