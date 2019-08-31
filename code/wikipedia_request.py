import requests

S = requests.Session()

URL = "https://pl.wikipedia.org/w/api.php"

SEARCHPAGE = "AGH"

PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": SEARCHPAGE
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

# if DATA['query']['search'][1]['title'] == SEARCHPAGE:
print(DATA['query']['search'][1]['snippet'])
