from src.common_utils.database.database_service import DatabaseProxy


def init_database():
    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    # basic greetings

    print(db.add_conversation(text="cześć", tag='greeting'))
    db.add_conversation(text="siemka", tag='greeting')
    db.add_conversation(text="hejooo", tag='greeting')
    db.add_conversation(text="witaj", tag='greeting')
    db.add_conversation(text="dzień dobry", tag='greeting')
    #
    db.add_conversation(text="jak się masz?", tag='greeting_response')
    db.add_conversation(text="co u Ciebie słychać?", tag='greeting_response')
    db.add_conversation(text="jak leci?", tag='greeting_response')

    # # nameChatbot
    #
    db.add_conversation(text="Nauczono mnie by nie odpowiadać obcym, najpierw się poznajmy ",
                        tag='no_introduction_message')

    db.add_conversation(text="jak masz na imię", tag='name_request')
    db.add_conversation(text="jak się nazywasz", tag='name_request')

    db.add_conversation(text="mam na imię , a Ty", tag='name_response')
    db.add_conversation(text="moje imię to , a Twoje", tag='name_response')
    db.add_conversation(text="nazwano mnie , a Ciebie?", tag='name_response')

    db.add_conversation(text="miło cię poznać", tag='name_response_end')
    db.add_conversation(text="bardzo mi miło", tag='name_response_end')

    # general conversation intro

    db.add_conversation(text="w czym mogę Ci pomóc?", tag='general_conversation_intro')
    db.add_conversation(text="o co chcesz mnie spytać?", tag='general_conversation_intro')

    db.add_conversation(text="Pepper", tag='my_name')

    # basic question

    db.add_conversation(text="u mnie wszystko okej", tag='basic_question_response')
    db.add_conversation(text="u mnie w porządku", tag='basic_question_response')
    db.add_conversation(text="wszystko super", tag='basic_question_response')
    db.add_conversation(text="jest okej", tag='basic_question_response')
    db.add_conversation(text="bez problemów", tag='basic_question_response')

    db.add_conversation(text=",miło że pytasz", tag='basic_question_response_end')
    db.add_conversation(text=", dzięki", tag='basic_question_response_end')
    #
    db.add_conversation(text="a Ty", tag='basic_question_request')
    db.add_conversation(text="jak się masz?", tag='basic_question_request')


