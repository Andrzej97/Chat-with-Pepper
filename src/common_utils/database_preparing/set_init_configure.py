import src.common_utils.custom_exceptions as Exceptions
import src.common_utils.database_preparing.csv_to_database_filler as scrapper_data
import src.common_utils.database_preparing.init_db_with_general_data as general_data
import src.common_utils.database_preparing.init_db_with_popular_data as popular_data
from configuration import Configuration as conf
from src.common_utils.database.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as Exceptions


def initialize_db_with_continue_statements(db):
    # fixme: to be removed after adding to database initialization file

    db.add_conversation(text="powiedzieć", tag='continue')
    db.add_conversation(text="więcej", tag='continue')
    # ------------------------------------------------------
    db.add_conversation(text="przykro mi, to wszystko co wiem", tag='cannot_say_more')
    db.add_conversation(text="to wszystko co wiem na ten temat", tag='cannot_say_more')
    db.add_conversation(text="nie wiem więcej", tag='cannot_say_more')
    db.add_conversation(text="na tę chwilę to musi wystarczyć", tag='cannot_say_more')


def initialize_db_with_popular_data(db):
    COLLECTION_NAME = conf.NUMBERS_QUEST_COLLECTION.value
    try:
        popular_data.initialize_db_with_numbers_questions(db, COLLECTION_NAME)
    except Exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(COLLECTION_NAME)
        popular_data.initialize_db_with_numbers_questions(db, COLLECTION_NAME)

    COLLECTION_NAME = conf.POPULAR_QUEST_COLLECTION.value
    try:
        popular_data.initialize_db_with_popular_questions(db, COLLECTION_NAME)
    except Exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(COLLECTION_NAME)
        popular_data.initialize_db_with_popular_questions(db, COLLECTION_NAME)


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
    file = open(path, mode='r', encoding='utf-8')
    lines = list(map(lambda x: x.rstrip(), list(file.readlines())))
    return lines


def create_collections(database):
    collections = [collection for collection in list(Configuration) if contains('collection', collection.name)]
    capped_collections = [capped_collection for capped_collection in collections if
                          contains('capped', capped_collection.name)]
    for collection in collections:
        try:
            database.create_new_collection(collection.value)
        except Exceptions.CollectionAlreadyExistsInDatabaseError:
            database.remove_collection(collection.value)
            database.create_new_collection(collection.value)
    for capped_collection in capped_collections:
        try:
            database.create_new_capped_collection(capped_collection.value)
        except Exceptions.CollectionAlreadyExistsInDatabaseError:
            database.remove_collection(capped_collection.value)
            database.create_new_capped_collection(capped_collection.value)


def contains(key, parameter):
    if type(parameter) is str:
        return key in parameter.lower()


def main():
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    create_collections(db)
    initialize_language_utils_database(db)
    general_data.init_database(db)
    #scrapper_data.initialize_main_collection_from_scrapper(db)
    initialize_db_with_continue_statements(db)
    initialize_db_with_popular_data(db)
    initialize_language_utils_database(db)
    scrapper_data.initialize_main_collection_from_scrapper(db)
    scrapper_data.inert_into_database('./csv_files/main_statements.csv', db)



if __name__ == '__main__':
    main()
