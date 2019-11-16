from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import re
from csvWriter import CsvWriter

# setting proper variables: names and paths:
ITERS_NUM = 2000                                                # number of iterations, used also in some file names
DATE = '191026'                                                 # for the purpose of file naming
STARTING_URL = "https://www.agh.edu.pl"
URLS_CSV_FILENAME = 'csv_files/urls_' + str(ITERS_NUM) + '.csv'           # suggested format: 'urls_<number_of_iterations>.csv'
DB_CSV_FILENAME = 'csv_files/db_' + DATE + '_' + str(ITERS_NUM) + '.csv'  # suggested format: 'db_<yymmdd>_<number_of_iterations>.csv'
urls_to_search = {STARTING_URL: False}                          # {<url>, <URL has already been searched for new links>}
polish_words_map = {}

def main():
    global urls_to_search
    CHROME_WEB_DRIVER = webdriver.Chrome(executable_path=r'C:\Users\User\chromedriver_win32\chromedriver.exe')
    DB_CSV_WRITER = CsvWriter(DB_CSV_FILENAME)
    i = 0
    while i < ITERS_NUM:
        url_to_search_through = get_next_url_to_search_through()
        if url_to_search_through is None:
            break
        CHROME_WEB_DRIVER.get(url_to_search_through)
        data = get_data(CHROME_WEB_DRIVER.page_source, url_to_search_through)
        save_data(data, DB_CSV_WRITER)
        urls_to_search[url_to_search_through] = True  # mark current URL as already searched
        other_relative_urls = find_other_relative_urls(CHROME_WEB_DRIVER.page_source)
        add_new_urls(other_relative_urls)
        i += 1
    save_urls_list()

def get_next_url_to_search_through():
    for url, wasSearched in urls_to_search.items():
        if wasSearched == False:
            return url
    return None

def get_data(content, url):
    tags = get_tags(url)
    soup = BeautifulSoup(content, features="html.parser")
    whole_page_text = ""
    for bodytext in soup.findAll("p", "bodytext"):
        text = str(bodytext)
        if len(text) > 50:
            first_letter = text.find('>') + 1
            text = text[first_letter:]
            last_letter = text.find('<')
            text = text[:last_letter]
            while len(text) > 0 and text[len(text) - 1] == '\n':
                text = text[:-1]
            if len(text) > 0:   # could be 0, for example:<p class="bodytext"><a class="external-link-new-window" href=...>
                whole_page_text += (' ' + text)
    return [tags, whole_page_text]

def get_tags(url):
    url = url[len(STARTING_URL):]
    tags = url.split('/')
    for i in range(len(tags)):
        tags[i] = tags[i].split('-')
    tags_list = list(itertools.chain.from_iterable(tags))
    for i in range(len(tags_list)):
        tags_list[i] = tags_list[i].lower()
        if tags_list[i] in polish_words_map:
            tags_list[i] = polish_words_map[tags_list[i]]
    tags_list.remove('')
    return tags_list

def save_data(data, DB_CSV_WRITER):
    tags = data[0]
    whole_page_text = data[1]
    if len(whole_page_text) > 20:
        DB_CSV_WRITER.write_tags_and_text(tags, whole_page_text)

def find_other_relative_urls(content):
    soup = BeautifulSoup(content, features="html.parser")
    relative_urls=[]
    for link in soup.find_all('a'):
        link_as_str = link.get('href')
        if link_as_str is None or link_as_str == '/':
            continue
        if is_relative(link_as_str):
            relative_urls.append(link_as_str)
            whole_link_str = str(link)
            words = re.split('\"|<|>|=|/|-| ', whole_link_str)
            for word in words:
                word = word.lower()
                if has_polish_char(word):
                    polish_words_map[delete_polish_chars(word)] = word
    delete_ending_slash(relative_urls)
    return relative_urls

def is_relative(link):
    str_len = len(link)
    if str_len <= 2:
        return False
    return link[0] == '/' and link[str_len - 1] == '/'

def has_polish_char(word):
    for letter in word:
        if letter in'ąćęłóśżź':
            return True
    return False

def delete_polish_chars(word):
    word = word.replace('ą', 'a')
    word = word.replace('ć', 'c')
    word = word.replace('ę', 'e')
    word = word.replace('ł', 'l')
    word = word.replace('ó', 'o')
    word = word.replace('ś', 's')
    word = word.replace('ż', 'z')
    word = word.replace('ź', 'z')
    return word

def delete_ending_slash(relative_urls):
    for i in range(len(relative_urls)):
        relative_urls[i] = relative_urls[i][:-1]

def add_new_urls(other_urls):
    for relative_url in other_urls:
        url = STARTING_URL + relative_url
        if url not in urls_to_search:
            urls_to_search[url] = False

def save_urls_list():
    urls_list = []
    for k, v, in urls_to_search.items():
        urls_list.append(k)
    df = pd.DataFrame({'url address': urls_list})
    df.to_csv(URLS_CSV_FILENAME, index=False, encoding='utf-8')

main()
