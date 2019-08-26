from chatterbot.storage import SQLStorageAdapter


def intitialize():
    db = SQLStorageAdapter()
    # sample greetings
    # db.create(text="cześć", in_response_to='hej', conversation='greeting')
    # db.create(text="siemka", in_response_to='hej', conversation='greeting')
    # db.create(text="hejooo", in_response_to='hej', conversation='greeting')
    # db.create(text="witaj", in_response_to='hej', conversation='greeting')
    # db.create(text="dzień dobry", in_response_to='hej', conversation='greeting')
