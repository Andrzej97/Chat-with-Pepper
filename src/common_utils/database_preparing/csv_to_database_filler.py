# zastanowic sie czy funkcja filter tags dziala tak jak powinna - raczej jest dobrze zaimplementowana, ale czy samo sentence_filter dziala tak jak tego oczekujemy
# pododdawac przy szukaniu tagów w zdaniach nawiasy () - sprawdzać początki, zastosować pętlę, aby liczyło się słowo postaci (word),

from src.common_utils.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as exceptions
import csv
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from csvWriter import CsvWriter

def try_to_expand(word):
    word = word.lower()
    if word == '+48':
        return '48'
    if word == '1.':
        return '1'
    if word == '100.':
        return '100'
    if word == 'al.':
        return 'aleje'
    if word == 'art.':
        return 'artykuł'
    if word == 'bip':
        return 'biuletyn informacji publicznej'
    if word == 'dkg':
        return 'dekagramów'
    if word == 'doc.':
        return 'docent'
    if word == 'dr':
        return 'doktor'
    if word == 'dra':
        return 'doktora'
    if word == 'drem':
        return 'doktorem'
    if word == 'drowi':
        return 'doktorowi'
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
    if word == 'ks.':
        return 'ksiądz'
    if word == 'łac.':
        return 'łaciny'
    if word == 'm.in.':
        return 'między innymi'
    if word == 'mgr':
        return 'magister'
    if word == 'mgra':
        return 'magistra'
    if word == 'mm':
        return 'milimetrów'
    if word == 'nadzw.':
        return 'nadzwyczajny'
    if word == 'n.s.d.a.p.':
        return 'narodowosocjalistycznej niemieckiej partii robotników'
    if word == 'np.':
        return 'na przykład'
    if word == 'nr':
        return 'numer'
    if word == 'nrf':
        return 'niemieckiej republiki federalnej'
    if word == 'nszz':
        return 'niezależny samorządowy związek zawodowy'
    if word == 'ok.':
        return 'około'
    if word == 'pr':
        return 'public relations'
    if word == 'prof.':
        return 'profesor'
    if word == 'r.':
        return 'roku'
    if word == 'r.,':
        return 'roku,'
    if word == 'tel.':
        return 'telefon'
    if word == 'tj.':
        return 'to jest'
    if word == 'tzw.':
        return 'tak zwany'
    if word == 'ust.':
        return 'ustawy'
    if word == 'wew.':
        return 'wewnętrzny'
    if word == 'wyd.':
        return 'wydanie'
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
    f_out_reader_writer = CsvWriter(file_out)
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

def main():
    # expand_shortcuts('db_191009_2000.csv', 'db_191009_2000_shortcuts_expanded.csv')

    # # to prepare necessary files from one file: DB_FINAL_num.csv
    # filter_tags('DB_FINAL_130.csv', 'DB_FINAL_130_TAGS_FILTERED.csv')
    # make_phrases_csv('DB_FINAL_130_TAGS_FILTERED.csv', 'DB_FINAL_130_PHRASES.csv')

    # to fill mongo database
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')

    collection = 'MAIN_COLLECTION'
    try:
        db.create_new_collection(collection)
    except exceptions.CollectionAlreadyExistsInDatabaseError:
        db.remove_collection(collection)
        db.create_new_collection(collection)
        print("Collection Already Exists Error")

    with open('DB_FINAL_130_TAGS_FILTERED.csv', encoding="utf-8") as csvfile:
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

    with open('DB_FINAL_130_PHRASES.csv', encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter='#')
        for row in readCSV:
            print(row)
            tags = row[:-1]
            text = row[-1:]
            db.add_doc_with_tags_list(collection, tags, text)

main()
