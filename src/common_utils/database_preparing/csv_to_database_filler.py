import src.common_utils.custom_exceptions as exceptions
import csv
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from csvWriter import CsvWriter
import os.path
from configuration import Configuration

def initialize_main_collection_from_scrapper(db):
    # to prepare necessary files from one file: DB_FINAL_<number>.csv
    if not os.path.exists('csv_files/DB_FINAL_150_TAGS_FILTERED.csv'):
        make_filter_tags_csv('csv_files/db_proven_150.csv', 'csv_files/DB_FINAL_150_TAGS_FILTERED.csv')
    if not os.path.exists('csv_files/DB_FINAL_100_PHRASES.csv'):
        make_phrases_csv('csv_files/db_provenForPhrases_100.csv', 'csv_files/DB_FINAL_100_PHRASES.csv')

    # to fill mongo database
    collection = 'MAIN_COLLECTION'
    try:
        db.create_new_collection(collection)
    except exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(collection)
        db.create_new_collection(collection)
        print("Collection Already Exists Error")
    with open('csv_files/DB_FINAL_150_TAGS_FILTERED.csv', encoding="utf-8") as csvfile:
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
    with open('csv_files/DB_FINAL_100_PHRASES.csv', encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter='#')
        for row in readCSV:
            print(row)
            tags = row[:-1]
            text = row[-1:]
            db.add_doc_with_tags_list(collection, tags, text)

def make_filter_tags_csv(in_file, out_file):
    csvWriter = CsvWriter(out_file)
    with open(in_file, encoding="utf-8") as f_in:
        readCSV = csv.reader(f_in, delimiter='#')
        sentence_filter = SentenceFilter()
        for row in readCSV:
            tags = row[:-1]
            text = row[-1:][0]
            tags_filtered = set()
            for tag in tags:
                filtered = sentence_filter.extract_complex_lemmas_and_filter_stopwords(tag)
                for elem in filtered:
                    tags_filtered.add(elem)
            if len(tags_filtered) != 0:
                csvWriter.write_tags_and_text(list(tags_filtered), text)
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
                tags_for_words = sentence_filter.extract_complex_lemmas_and_filter_stopwords(phrase)
                if len(tags_for_words) != 0:
                    csvWriter.write_tags_and_text(tags_for_words, phrase)