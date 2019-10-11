from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import re
from csvReaderWriter import CsvReaderWriter

def main():
    # print(get_tags("https://www.agh.edu.pl", "https://www.agh.edu.pl/info/article/101-inauguracja-roku-akademickiego-glowne-obchody-jubileuszu-100-lecia-agh", {}))
    all_urls_dict_and_database = find_all_urls("https://www.agh.edu.pl")
    all_urls_dict = all_urls_dict_and_database[0]
    database = all_urls_dict_and_database[1]
    all_urls = dict_to_list_of_keys(all_urls_dict)
    df = pd.DataFrame({'url address':all_urls})
    df.to_csv('urls_2000.csv', index=False, encoding='utf-8')
    df2 = pd.DataFrame({'TAGS#TEXT':database})
    df2.to_csv('database_2000.csv', index=False, encoding='utf-8')

def find_all_urls(starting_url):
    driver = webdriver.Chrome(executable_path=r'C:\Users\User\chromedriver.exe')
    all_urls = {starting_url: False}  # {url, was searched for new links}
    database = []
    polish_names_map = {}
    csvReaderWriter = CsvReaderWriter('db_191009_2000.csv')
    i = 0
    while i < 2000:
        url_to_search_through = get_next_url_to_search_through(all_urls)
        if url_to_search_through is None:
            break
        driver.get(url_to_search_through)
        get_data(database, driver.page_source, starting_url, url_to_search_through, polish_names_map, csvReaderWriter)
        other_relative_urls = find_other_relative_urls_and_get_data(driver.page_source, polish_names_map)
        delete_ending_slash(other_relative_urls)
        # print(other_relative_urls)
        update_urls(all_urls, other_relative_urls, starting_url)
        # print(url_to_search_through)
        all_urls[url_to_search_through] = True
        i += 1
    print(polish_names_map)
    return [all_urls, database]

def get_next_url_to_search_through(urls):
    for url, wasSearched in urls.items():
        if wasSearched == False:
            return url
    return None

def get_data(database, content, base_url, url, names_map, csvReaderWriter):
    print(url)
    tags = get_tags(base_url, url, names_map)
    soup = BeautifulSoup(content, features="html.parser")
    whole_page_text = ""
    for bodytext in soup.findAll("p", "bodytext"):
        text = str(bodytext)
        # print('Before if:')
        # print(text)
        if len(text) > 50:
            first_letter = text.find('>') + 1
            text = text[first_letter:]
            last_letter = text.find('<')
            text = text[:last_letter]
            while len(text) > 0 and text[len(text) - 1] == '\n':
                text = text[:-1]
            # print("Text: ")
            # print('Inside if:')
            # print(text)
            if len(text) > 0:   # could be 0, for example:<p class="bodytext"><a class="external-link-new-window" href=...>
                whole_page_text += (' ' + text)
    if len(whole_page_text) > 20:
        database.append(str(tags) + '#' + whole_page_text)
        csvReaderWriter.write_tags_and_text(tags, whole_page_text)

def get_tags(base_url, url, names_map):
    url = url[len(base_url):]
    print('SHORTEN URL:', url)
    tags = url.split('/')
    for i in range(len(tags)):
        tags[i] = tags[i].split('-')
    tags_list = list(itertools.chain.from_iterable(tags))
    for i in range(len(tags_list)):
        tags_list[i] = tags_list[i].lower()
        if tags_list[i] in names_map:
            tags_list[i] = names_map[tags_list[i]]
    tags_list.remove('')
    return tags_list


def find_other_relative_urls_and_get_data(content, names_map):
    soup = BeautifulSoup(content, features="html.parser")
    relative_urls=[]
    for link in soup.find_all('a'):
        link_as_str = link.get('href')
        if link_as_str is None or link_as_str == '/':
            continue
        if is_relative(link_as_str):
            # print('LINK:\t\t', link)
            # print('LINK_STR:\t', link_as_str)
            relative_urls.append(link_as_str)
            whole_link_str = str(link)
            # print(whole_link_str)
            words = re.split('\"|<|>|=|/|-| ', whole_link_str)
            print(words)
            for word in words:
                word = word.lower()
                if has_polish_char(word):
                    names_map[delete_polish_chars(word)] = word
    return relative_urls

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

def is_relative(link):
    str_len = len(link)
    if str_len <= 2:
        return False
    return link[0] == '/' and link[str_len - 1] == '/'

def delete_ending_slash(relative_urls):
    for i in range(len(relative_urls)):
        relative_urls[i] = relative_urls[i][:-1]

def update_urls(urls, other_urls, starting_url):
    for relative_url in other_urls:
        url = starting_url + relative_url
        if url not in urls:
            urls[url] = False

def dict_to_list_of_keys(all_urls):
    new_list = []
    for k, v, in all_urls.items():
        new_list.append(k)
    return new_list

main()