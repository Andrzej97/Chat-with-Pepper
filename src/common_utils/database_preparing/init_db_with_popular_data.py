from src.common_utils.database.database_service import DatabaseProxy

def initialize_db_with_numbers_questions(db, COLLECTION_NAME):

    db.create_new_collection(COLLECTION_NAME)
    db.add_new_doc_to_collection(COLLECTION_NAME, {'tags': ['rektor'],
                                                   'text': 'Rektorem uczelni jest profesor doktor habilitowany '
                                                                               'Tadeusz Słomka'})



def initialize_db_with_popular_questions(db, COLLECTION_NAME):
    db.create_new_collection(COLLECTION_NAME)
    db.add_new_doc_to_collection(COLLECTION_NAME, {'tags': ['kierunek'],
                                                   'text': 'Na akademi górniczo hutniczej działa 62 kierunki'})


