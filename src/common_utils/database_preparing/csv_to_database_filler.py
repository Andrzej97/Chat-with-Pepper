from src.common_utils.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as exceptions
import csv
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter

def correct_csv_format(file_in, file_out, file_out_phrases):
    f_out = open(file_out, encoding="utf-8", mode="w")
    f_out_phrases = open(file_out_phrases, encoding="utf-8", mode="w")

    with open(file_in, encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile)
        sentence_filter = SentenceFilter()
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

            # print('PLAIN_TEXT:\t', plain_text)
            splitted_plain_text = plain_text[:-1].split('.')
            for phrase in splitted_plain_text:
                # print('Splitted:\t', phrase)'
                if phrase == '':
                    continue
                f_out_phrases.write(phrase)
                phrase_splitted = phrase.split()
                for word in phrase_splitted:
                    # print('Word:\t\t', word)
                    if word[len(word) - 1] == ',':
                        word = word[:-1]
                        # print('Word after if:\t', word)
                    filtered = sentence_filter.filter_sentence(word)
                    if len(filtered) != 0:
                        # print('filtered:\t', filtered[0][0])
                        f_out_phrases.write('#' + filtered[0][0])
                f_out_phrases.write("\n")

            f_out.write(plain_text)
            for elem in tags_list:
                #delete starting and ending [...]
                elem = elem[1 : len(elem) - 1]
                # print('elem:\t\t', elem)
                filtered = sentence_filter.filter_sentence(elem)
                if len(filtered) != 0:
                    # print('filtered:\t', filtered[0][0])
                    f_out.write('#' + filtered[0][0])
            # f_out.write(row_str)
            f_out.write("\n")

    f_out.close()
    f_out_phrases.close()

def main():
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')

    correct_csv_format('database_100.csv', 'database_correct_filtered_100.csv', 'database_filtered_phrases_100.csv')

    collection = 'MAIN_COLLECTION'
    try:
        db.create_new_collection(collection)
    except exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(collection)
        db.create_new_collection(collection)
        print("Collection Already Exists Error")

    with open('database_correct_filtered_100.csv', encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter='#')
        for row in readCSV:
            tags = row[1:len(row)]
            text = row[0]
            db.add_doc_with_tags_list(collection, tags, text)

    # checking if it worked
    print(db.get_docs_from_collection_by_tags_list(collection, ['historia']))


    collection = 'PHRASES'
    try:
        db.create_new_collection(collection)
    except exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(collection)
        db.create_new_collection(collection)
        print("Collection Already Exists Error")

    with open('database_filtered_phrases_100.csv', encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter='#')
        for row in readCSV:
            print(row)
            tags = row[1:len(row)]
            text = row[0]
            db.add_doc_with_tags_list(collection, tags, text)



main()
