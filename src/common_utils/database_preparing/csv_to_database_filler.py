from src.common_utils.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as exceptions
import csv
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from csvWriter import CsvWriter

def make_filter_tags_csv(in_file, out_file):
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

def make_phrases_csv(in_file, out_file):
    csvWriter = CsvWriter(out_file)
    with open(in_file, encoding="utf-8") as f_in:
        readCSV = csv.reader(f_in, delimiter='#')
        sentence_filter = SentenceFilter()
        for row in readCSV:
            text = row[-1:][0]
            phrases = text.split('.')
            for phrase in phrases:
                tags_for_words = sentence_filter.andrzej_extract_lemmas_and_filter_stopwords(phrase)
                if len(tags_for_words) != 0:
                    csvWriter.write_tags_and_text(tags_for_words, phrase)

def main():
    # # to prepare necessary files from one file: DB_FINAL_<number>.csv
    # make_filter_tags_csv('DB_FINAL_150.csv', 'DB_FINAL_150_TAGS_FILTERED.csv')
    # make_phrases_csv('DB_FINAL_150.csv', 'DB_FINAL_150_PHRASES.csv')

    # to fill mongo database
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')

    collection = 'MAIN_COLLECTION'
    try:
        db.create_new_collection(collection)
    except exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(collection)
        db.create_new_collection(collection)
        print("Collection Already Exists Error")

    with open('DB_FINAL_150_TAGS_FILTERED_2.csv', encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter='#')
        for row in readCSV:
            tags = row[:-1]
            text = row[-1:]
            db.add_doc_with_tags_list(collection, tags, text)

    collection = 'PHRASES'
    try:
        db.create_new_collection(collection)
    except exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(collection)
        db.create_new_collection(collection)
        print("Collection Already Exists Error")

    with open('DB_FINAL_150_PHRASES_2.csv', encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter='#')
        for row in readCSV:
            print(row)
            tags = row[:-1]
            text = row[-1:]
            db.add_doc_with_tags_list(collection, tags, text)

main()
