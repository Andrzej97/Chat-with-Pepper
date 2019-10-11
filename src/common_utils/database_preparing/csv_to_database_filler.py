from src.common_utils.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as exceptions
import csv
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from csvReaderWriter import CsvReaderWriter

def try_to_expand(word):
    word = word.lower()
    if word == '100.':
        return '100'
    if word == 'al.':
        return 'aleje'
    if word == 'art.':
        return 'artykuł'
    if word == 'doc.':
        return 'docent'
    if word == 'dr':
        return 'doktor'
    if word == 'ds.':
        return 'do spraw'
    if word == 'ew.':
        return 'ewentualnie'
    if word == 'hab.':
        return 'habilitowany'
    if word == 'im.':
        return 'imienia'
    if word == 'inż.':
        return 'inżynier'
    if word == 'itp.':
        return 'i tym podobne'
    if word == 'łac.':
        return 'łaciny'
    if word == 'm.in.':
        return 'między innymi'
    if word == 'mgr':
        return 'magister'
    if word == 'ok.':
        return 'około'
    if word == 'prof.':
        return 'profesor'
    if word == 'r.':
        return 'roku'
    if word == 'r.,':
        return 'roku,'
    if word == 'tj.':
        return 'to jest'
    if word == 'ust.':
        return 'ustawy'
    return word

def expand_text_shortcuts(text):
    words = text.split()
    # print(words)
    for i in range(len(words)):
        words[i] = try_to_expand(words[i])
    final_text = ''
    for i in range(len(words)):
        final_text += words[i] + ' '
    final_text = final_text[:-1]
    return final_text

def expand_shortcuts(file_in, file_out):
    f_out_reader_writer = CsvReaderWriter(file_out)
    with open(file_in, encoding="utf-8") as csv_file:
        read_csv = csv.reader(csv_file, delimiter='#')
        for row in read_csv:
            text = row[len(row) - 1]
            row[len(row) - 1] = expand_text_shortcuts(text)
            # print(text)
            tags = row[:-1]
            text = row[len(row) - 1]
            print('TAGS:\t', tags)
            print('TEXT:\t', text)
            f_out_reader_writer.write_tags_and_text(tags, text)

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
            tags_str = row_splitted_to_tags_and_text[:-1]
            plain_text = row_splitted_to_tags_and_text[len(row_splitted_to_tags_and_text) - 1]
            # delete starting and ending [...] in tags
            # tags_str = tags_str[1 : len(tags_str) - 1]
            # print(tags_str)
            # print(plain_text)
            # tags_list = tags_str.split(', ')
            # delete first empty element: ''
            tags_list = tags_str

            # print('PLAIN_TEXT:\t', plain_text)
            splitted_plain_text = plain_text[:-1].split('.')
            for phrase in splitted_plain_text:
                # print('Splitted:\t', phrase)'
                if phrase == '':
                    continue
                f_out_phrases.write(phrase.strip())
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
    # db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')

    # expand_shortcuts('db_191009_2000.csv', 'db_191009_2000_noShortcuts.csv')
    correct_csv_format('db_191009_2000_noShortcuts.csv', 'db_191009_2000_noShortcuts_tagsFiltered.csv', 'db_191009_2000_noShortcuts_phrases.csv')
    #
    # collection = 'MAIN_COLLECTION'
    # try:
    #     db.create_new_collection(collection)
    # except exceptions.CollectionAlreadyExistsInDatabaseError:
    #     db.remove_collection(collection)
    #     db.create_new_collection(collection)
    #     print("Collection Already Exists Error")
    #
    # with open('database_correct_filtered_100.csv', encoding="utf-8") as csvfile:
    #     readCSV = csv.reader(csvfile, delimiter='#')
    #     for row in readCSV:
    #         tags = row[1:len(row)]
    #         text = row[0]
    #         db.add_doc_with_tags_list(collection, tags, text)
    #
    # # checking if it worked
    # print(db.get_docs_from_collection_by_tags_list(collection, ['historia']))
    #
    #
    # collection = 'PHRASES'
    # try:
    #     db.create_new_collection(collection)
    # except exceptions.CollectionAlreadyExistsInDatabaseError:
    #     db.remove_collection(collection)
    #     db.create_new_collection(collection)
    #     print("Collection Already Exists Error")
    #
    # with open('database_filtered_phrases_100.csv', encoding="utf-8") as csvfile:
    #     readCSV = csv.reader(csvfile, delimiter='#')
    #     for row in readCSV:
    #         print(row)
    #         tags = row[1:len(row)]
    #         text = row[0]
    #         db.add_doc_with_tags_list(collection, tags, text)
    #


main()
