# zastanowic sie czy funkcja filter tags dziala tak jak powinna - raczej jest dobrze zaimplementowana, ale czy samo sentence_filter dziala tak jak tego oczekujemy
# pododdawac przy szukaniu tagów w zdaniach nawiasy () - sprawdzać początki, zastosować pętlę, aby liczyło się słowo postaci (word),

from src.common_utils.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as exceptions
import csv
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from csvWriter import CsvWriter
import morfeusz2

def filter_tags(in_file, out_file):
    csvWriter = CsvWriter(out_file)
    with open(in_file, encoding="utf-8") as f_in:
        readCSV = csv.reader(f_in, delimiter='#')
        sentence_filter = SentenceFilter()
        for row in readCSV:
            tags = row[:-1]
            text = row[-1:][0]
            tags_filtered = []
            for tag in tags:
                filtered = sentence_filter.filter_sentence(tag)
                if len(filtered) != 0:
                    tags_filtered.append(filtered[0][0])
            if len(tags_filtered) != 0:
                csvWriter.write_tags_and_text(tags_filtered, text)
            else:
                csvWriter.write_tags_and_text(tags, text)
            print('TAGS: ', tags)
            print('TAGS FILTERED: ', tags_filtered)
            print('TEXT: ', text)

def make_phrases_csv(in_file, out_file):
    csvWriter = CsvWriter(out_file)
    with open(in_file, encoding="utf-8") as f_in:
        readCSV = csv.reader(f_in, delimiter='#')
        sentence_filter = SentenceFilter()
        for row in readCSV:
            text = row[-1:][0]
            phrases = text.split('.')
            print('TEXT:\t', text)
            for phrase in phrases:
                print('PHRASE:\t', phrase)
                words = phrase.split()
                print('WORDS:\t', words)
                tags_for_words = []
                for word in words:
                    to_filter = word
                    if to_filter[-1:] in {':', ';', ','}:
                        to_filter = to_filter[:-1]
                    filtered = sentence_filter.filter_sentence(to_filter)
                    if len(filtered) != 0:
                        tags_for_words.append(filtered[0][0])
                if len(tags_for_words) != 0:
                    csvWriter.write_tags_and_text(tags_for_words, phrase)
                print('WORDS TAGS:\t', tags_for_words)

def delete_additional_info_after_colon(word):
    index = word.find(':')
    if index == -1:
        return word
    return word[:index]

def set_to_str_with_colons(set):
    string = ''
    for elem in set:
        string += elem + ':'
    string = string[:-1]
    return string

def filter_tags_2(in_file, out_file):
    csvWriter = CsvWriter(out_file)
    with open(in_file, encoding="utf-8") as f_in:
        readCSV = csv.reader(f_in, delimiter='#')
        sentence_filter = SentenceFilter()
        for row in readCSV:
            tags = row[:-1]
            text = row[-1:][0]
            tags_filtered = []
            for tag in tags:
                filtered = sentence_filter.andrzej_extract_lemmas_and_filter_stopwords(tag)
                for elem in filtered:
                    tags_filtered.append(elem)
            if len(tags_filtered) != 0:
                csvWriter.write_tags_and_text(tags_filtered, text)
            else:
                csvWriter.write_tags_and_text(tags, text)
            # print('TAGS: ', tags)
            # print('TAGS FILTERED: ', tags_filtered)
            # print('TEXT: ', text)

def make_phrases_csv_2(in_file, out_file):
    csvWriter = CsvWriter(out_file)
    with open(in_file, encoding="utf-8") as f_in:
        readCSV = csv.reader(f_in, delimiter='#')
        sentence_filter = SentenceFilter()
        for row in readCSV:
            text = row[-1:][0]
            phrases = text.split('.')
            # print('TEXT:\t', text)
            for phrase in phrases:
                # print('PHRASE:\t', phrase)

                tags_for_words = sentence_filter.andrzej_extract_lemmas_and_filter_stopwords(phrase)

                if len(tags_for_words) != 0:
                    csvWriter.write_tags_and_text(tags_for_words, phrase)
                # print('WORDS TAGS:\t', tags_for_words)

def main():
    # # expand_shortcuts('db_191009_2000.csv', 'db_191009_2000_shortcuts_expanded.csv')
    #
    # # # to prepare necessary files from one file: DB_FINAL_num.csv
    # # filter_tags('DB_FINAL_150.csv', 'DB_FINAL_150_TAGS_FILTERED.csv')
    # # make_phrases_csv('DB_FINAL_150_TAGS_FILTERED.csv', 'DB_FINAL_150_PHRASES.csv')

    ## new_make_phrases_csv('test.csv', 'test_PHRASES_NEW.csv')

    filter_tags_2('DB_FINAL_150.csv', 'DB_FINAL_150_TAGS_FILTERED_2.csv')
    make_phrases_csv_2('DB_FINAL_150.csv', 'DB_FINAL_150_PHRASES_2.csv')

    # # to fill mongo database
    # db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    #
    # collection = 'MAIN_COLLECTION'
    # try:
    #     db.create_new_collection(collection)
    # except exceptions.CollectionAlreadyExistsInDatabaseError:
    #     db.remove_collection(collection)
    #     db.create_new_collection(collection)
    #     print("Collection Already Exists Error")
    #
    # with open('DB_FINAL_150_TAGS_FILTERED_2.csv', encoding="utf-8") as csvfile:
    #     readCSV = csv.reader(csvfile, delimiter='#')
    #     for row in readCSV:
    #         tags = row[:-1]
    #         text = row[-1:]
    #         db.add_doc_with_tags_list(collection, tags, text)
    #
    # collection = 'PHRASES'
    # try:
    #     db.create_new_collection(collection)
    # except exceptions.CollectionAlreadyExistsInDatabaseError:
    #     db.remove_collection(collection)
    #     db.create_new_collection(collection)
    #     print("Collection Already Exists Error")
    #
    # with open('DB_FINAL_150_PHRASES_2.csv', encoding="utf-8") as csvfile:
    #     readCSV = csv.reader(csvfile, delimiter='#')
    #     for row in readCSV:
    #         print(row)
    #         tags = row[:-1]
    #         text = row[-1:]
    #         db.add_doc_with_tags_list(collection, tags, text)

main()
