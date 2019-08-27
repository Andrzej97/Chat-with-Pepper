from chatterbot.storage import SQLStorageAdapter

db = SQLStorageAdapter(database_uri='sqlite:///./db.sqlite13')
db.create(text="cześć", in_response_to='hej', conversation='greeting')
db.create(text="siemka", in_response_to='hej', conversation='greeting')
db.create(text="hejooo", in_response_to='hej', conversation='greeting')
db.create(text="witaj", in_response_to='hej', conversation='greeting')
db.create(text="dzień dobry", in_response_to='hej', conversation='greeting')

db.create(text="jak się masz?", conversation='greeting_response')
db.create(text="co u Ciebie słychać?", conversation='greeting_response')
db.create(text="jak leci?", conversation='greeting_response')

print(db.create(text="jak masz na imię", conversation='name_request'))
print(db.create(text="jak się nazywasz", conversation='name_request'))
print(db.create(text="mam na imię ", conversation='name_response'))
print(db.create(text="moje imię to ", conversation='name_response'))
print(db.create(text="nazwano mnie ", conversation='name_response'))
print(db.create(text="Pepper", conversation='my_name'))

db.create(text="u mnie wszystko okej", conversation='basic_question_response')
db.create(text="u mnie w porządku", conversation='basic_question_response')
db.create(text="wszystko super", conversation='basic_question_response')
db.create(text="jest okej", conversation='basic_question_response')
db.create(text="bez problemów", conversation='basic_question_response')

db.create(text=",miło że pytasz", conversation='basic_question_response_end')
db.create(text=", dzięki", conversation='basic_question_response_end')

db.create(text="a Ty", conversation='basic_question_request')
db.create(text="jak się masz?", conversation='basic_question_request')

