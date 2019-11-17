from src.common_utils.database.database_service import DatabaseProxy

def initialize_db_with_popular_questions(db, COLLECTION_NAME):

    db.create_new_collection(COLLECTION_NAME)
    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['rektor', 'uczelnia', 'aktualny'], 'Rektorem uczelni jest profesor doktor habilitowany Tadeusz Słomka')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['miasteczko', 'studencki', 'uczelnia'], 'Miasteczko studenckie agh to najbardziej popularny kampus studencki w Polsce')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['agh', 'założenie', 'rok'], 'Akademia górniczo hutnicza została założona w 1919 roku')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['juwenalia', 'uczelnia', 'krakowski'], 'Najpopularniejsze juwenalia w Krakowie odbywają się na miasteczku studenckim agh'
                                            ' najczęściej w drugiej połowie maja')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['informatyk', 'wydział', 'centrum'], 'Centrum informatyki agh znajduje się przy ul Kawiory w budynku D17')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['uczelnia', 'imię'], 'Akademia górniczo hutnicza nosi imię Stanisława Staszica')



def initialize_db_with_numbers_questions(db, COLLECTION_NAME):
    db.create_new_collection(COLLECTION_NAME)
    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['uczelnia', 'kierunek'], 'Na akademi górniczo hutniczej działa 62 kierunki')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['uczelnia', 'student'], 'Na akademi górniczo hutniczej studiuje około 27 i pół tysiąca studentów'
                                              ' włączając słuchaczy studiów podyplomowych ')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['studia', 'stacjonarny', 'pierwszy', 'drugi', 'student'], 'Na akademi górniczo hutniczej na studia stacjonarne'
                                            ' pierwszego  i drugiego stopnia uczęszcza ponad 20 tysięcy studentów')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['studia', 'niestacjonarny', 'pierwszy', 'drugi', 'student'], 'Na studia niestacjonarne'
                                            ' pierwszego  i drugiego stopnia uczęszcza około 3 o pół tysiąca studentów')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['studia', 'doktor', 'doktorancki', 'doktorant'], 'Na studia doktoranckie stacjonarne i niestacjonarne uczęszcza ponad tysiąc doktorantów')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['studia', 'podyplomowy','student'], 'Na studiach podyplomowych na akademi górniczo hutniczej studiuje ponad 2 i pół tysiąca studentów')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['studia', 'podyplomowy', 'student'], 'Na studiach podyplomowych na akademi górniczo hutniczej studiuje ponad 2 i pół tysiąca studentów')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['uczelnia', 'obcokrajowiec', 'student', 'studiować'], 'Na akademi górniczo hutniczej studiuje prawie siedemset obcokrajowców')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['uczelnia', 'pracownik', 'dydaktyczny', 'naukowy'], 'uczelnia zatrudnia ponad 4 tysiące pracowników w tym pracownicy naukowo dydaktyczni w liczbie'
                      ' ponad tysiąc osiemset osób pracownicy dydaktyczni ponad dwieście siedemdziesiąt osób dyplomowani bibliotekarze 6 osób')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['dom', 'studencki', 'akademik', 'uczelnia'], 'akademia górniczo hutnicza posiada 19 domów studenckich dla studentów i gości')

    db.add_doc_with_tags_list(COLLECTION_NAME,
    ['uczelnia', 'wydział'], 'akademia górniczo hutnicza prowadzi studia na szesnastu wydziałach')