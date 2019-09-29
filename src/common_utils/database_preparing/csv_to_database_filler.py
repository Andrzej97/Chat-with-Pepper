from src.common_utils.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as exceptions
import csv

def correct_csv_format(file_in, file_out):
    f_out = open(file_out, encoding="utf-8", mode="w")

    with open(file_in, encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            row_str = str(row)
            if row_str == '''['TAGS#TEXT']''':
                continue
            # print(row_str)
            # deleting starting and ending [" ... "]
            row_str = row_str[2 : len(row_str) - 2]
            # print(row_str)
            row_splitted_to_tags_and_text = row_str.split('#')
            tags_str =row_splitted_to_tags_and_text[0]
            plain_text = row_splitted_to_tags_and_text[1]
            # delete starting and ending [...] in tags
            tags_str = tags_str[1 : len(tags_str) - 1]
            # print(tags_str)
            # print(plain_text)
            tags_list = tags_str.split(', ')
            # delete first empty element: ''
            tags_list = tags_list[1:]
            f_out.write(plain_text)
            for elem in tags_list:
                #delete starting and ending [...]
                elem = elem[1 : len(elem) - 1]
                # print('elem:', elem)
                f_out.write('#' + elem)
            # f_out.write(row_str)
            f_out.write("\n")

    f_out.close()

def main():
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')

    correct_csv_format('database_100.csv', 'database_correct_100.csv')

    collection = 'MAIN_COLLECTION'
    try:
        db.create_new_collection(collection)
    except exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(collection)
        db.create_new_collection(collection)
        print("Collection Already Exists Error")

    with open('database_correct.csv', encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter='#')
        for row in readCSV:
            tags = row[1:len(row)]
            text = row[0]
            db.add_doc_with_tags_list(collection, tags, text)

    # checking if it worked
    print(db.get_docs_from_collection_by_tags_list(collection, ['historia']))

main()
