from src.common_utils.database.database_service import DatabaseProxy

def initialize_db_with_popular_questions(db, COLLECTION_NAME):

    db.create_new_collection(COLLECTION_NAME)
    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['rektor', 'uczelnia'], 'text': 'Rektorem uczelni jest profesor doktor habilitowany Tadeusz Słomka'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['miasteczko', 'studencki'], 'text': 'Miasteczko studenckie agh to najbardziej popularny kampus studencki w Polsce'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['agh', 'założenie'], 'text': 'Akademia górniczo hutnicza została założona w 1919 roku'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['juwenalia', 'uczelnia', 'krakowski'], 'text': 'Najpopularniejsze juwenalia w Krakowie odbywają się na miasteczku studenckim agh'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['informatyka', 'wydział'], 'text': 'Centrum informatyki agh znajduje się przy ul. Kawiory w budynku D17'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['uczelnia', 'imię'], 'text': 'Akademia górniczo hutnicza nosi imię Stanisława Staszica'})



def initialize_db_with_numbers_questions(db, COLLECTION_NAME):
    db.create_new_collection(COLLECTION_NAME)
    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['uczelnia', 'kierunek'], 'text': 'Na akademi górniczo hutniczej działa 62 kierunki'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['uczelnia', 'student'], 'text': 'Na akademi górniczo hutniczej studiuje około 27 i pół tysiąca studentów'
                                              ' włączając słuchaczy studiów podyplomowych '})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['studia', 'stacjonarny', 'pierwszy', 'drugi', 'student'], 'text': 'Na akademi górniczo hutniczej na studia stacjonarne'
                                            ' pierwszego  i drugiego stopnia uczęszcza ponad 20 tysięcy studentów'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['studia', 'niestacjonarny', 'pierwszy', 'drugi', 'student'], 'text': 'Na studia niestacjonarne'
                                            ' pierwszego  i drugiego stopnia uczęszcza około 3 o pół tysiąca studentów'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['studia', 'doktor', 'doktorancki', 'doktorant'], 'text': 'Na studia doktoranckie stacjonarne i niestacjonarne uczęszcza ponad tysiąc doktorantów'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['studia', 'podyplomowy','student'], 'text': 'Na studiach podyplomowych na akademi górniczo hutniczej studiuje ponad 2 i pół tysiąca studentów'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['studia', 'podyplomowy', 'student'], 'text': 'Na studiach podyplomowych na akademi górniczo hutniczej studiuje ponad 2 i pół tysiąca studentów'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['uczelnia', 'obcokrajowiec', 'student', 'studiować'], 'text': 'Na akademi górniczo hutniczej studiuje prawie siedemset obcokrajowców'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['uczelnia', 'pracownik', 'dydaktyczny', 'naukowy'], 'text': 'uczelnia zatrudnia ponad 4 tysiące pracowników w tym pracownicy naukowo-dydaktyczni w liczbie'
                      ' ponad tysiąc osiemset osób pracownicy dydaktyczni ponad dwieście siedemdziesiąt osób dyplomowani bibliotekarze 6 osób'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['dom', 'studencki', 'akademik', 'uczelnia'], 'text': 'akademia górniczo hutnicza posiada 19 domów studenckich dla studentów i gości'})

    db.add_new_doc_to_collection(COLLECTION_NAME,
    {'tags': ['uczelnia', 'wydział'], 'text': 'akademia górniczo hutnicza prowadzi studia na szesnastu wydziałach'})