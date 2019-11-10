from src.common_utils.database.database_service import DatabaseProxy
import src.common_utils.database_preparing.initialize_database as general_data
import src.common_utils.database_preparing.csv_to_database_filler as scrapper_data


def initialize_language_utils_database(db):
    """
        run this method just when you use this code first time to initialize database with words from file
    """
    path = "./polish_stopwords.txt"  # in case of errors make sure that path is ok, `os.getcwd()` command is useful
    #db.create_new_collection('polish_stop_words')
    result = from_txt_file_to_list(path)
    list = []
    for r in result:
        list.append({'text': r})
    db.add_many_new_docs_to_collection('polish_stop_words', list)


def from_txt_file_to_list(path):
    file = open(path, mode='r', encoding='utf-8')
    lines = list(map(lambda x: x.rstrip(), list(file.readlines())))
    return lines


def main():
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    initialize_language_utils_database(db)
    general_data.init_database(db)
    scrapper_data.initialize_main_collection_from_scrapper(db)



if __name__ == '__main__':
    main()