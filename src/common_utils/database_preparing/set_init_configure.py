import src.common_utils.custom_exceptions as Exceptions
import src.common_utils.database_preparing.csv_to_database_filler as scrapper_data
from configuration import Configuration
from src.common_utils.database.database_service import DatabaseProxy


def insert_polish_stop_words(db):
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
    insert_polish_stop_words(db)
    scrapper_data.initialize_main_collection_from_scrapper(db)
    scrapper_data.inert_into_database('./csv_files/main_statements.csv', db)


if __name__ == '__main__':
    main()
