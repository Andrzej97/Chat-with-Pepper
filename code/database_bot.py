from chatterbot import ChatBot

# Uncomment the following lines to enable verbose logging
import logging

from chatterbot.storage import SQLStorageAdapter

logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot(
    'SQLMemoryTerminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///db.sqlite3',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ]
)

db = SQLStorageAdapter()
# db.create(text="cześć", in_response_to='hej', conversation='greeting')
# db.create(text="siemka", in_response_to='hej', conversation='greeting')
# db.create(text="hejooo", in_response_to='hej', conversation='greeting')
# db.create(text="witaj", in_response_to='hej', conversation='greeting')
# db.create(text="dzień dobry", in_response_to='hej', conversation='greeting')
words = db.filter(conversation='greeting')

for w in words:
    print(w)

# Get a few responses from the bo