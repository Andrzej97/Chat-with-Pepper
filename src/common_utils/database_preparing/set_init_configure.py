import src.common_utils.database_preparing.csv_to_database_filler as scrapper_data
import src.common_utils.database_preparing.initialize_database as general_data
from configuration import Configuration
from src.common_utils.database.database_service import DatabaseProxy


def initialize_db_with_continue_statements(db):
    # fixme: to be removed after adding to database initialization file

    db.add_conversation(text="powiedzieć", tag='continue')
    db.add_conversation(text="więcej", tag='continue')
    # ------------------------------------------------------
    db.add_conversation(text="przykro mi, to wszystko co wiem", tag='cannot_say_more')
    db.add_conversation(text="to wszystko co wiem na ten temat", tag='cannot_say_more')
    db.add_conversation(text="nie wiem więcej", tag='cannot_say_more')
    db.add_conversation(text="na tę chwilę to musi wystarczyć", tag='cannot_say_more')


def initialize_language_utils_database(db):
    """
        run this method just when you use this code first time to initialize database with words from file
    """
    path = "./polish_stopwords.txt"  # in case of errors make sure that path is ok, `os.getcwd()` command is useful
    # db.create_new_collection('polish_stop_words')
    result = from_txt_file_to_list(path)
    list = []
    for r in result:
        list.append({'text': r})
    db.add_many_new_docs_to_collection('polish_stop_words', list)


def from_txt_file_to_list(path):
    file = open(path, "r")
    lines = list(map(lambda x: x.rstrip(), list(file.readlines())))
    return lines


def create_collections(database):
    collections = [collection for collection in list(Configuration) if contains('collection', collection.name)]
    capped_collections = [capped_collection for capped_collection in collections if
                          contains('capped', capped_collection.name)]
    for collection in collections:
        database.create_new_collection(collection.value)
    for capped_collection in capped_collections:
        database.create_new_capped_collection(capped_collection)


def contains(key, parameter):
    if type(parameter) is str:
        return key in parameter.lower()


def main():
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    create_collections(db)
    initialize_language_utils_database(db)
    general_data.init_database(db)
    scrapper_data.initialize_main_collection_from_scrapper(db)
    initialize_db_with_continue_statements(db)


if __name__ == '__main__':
    main()
