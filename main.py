import pymongo

from src.general_chatbot import intro_conversation_bot
from src.common_utils import initialize_database
from src.common_utils.database_service import DatabaseProxy
import src.common_utils.custom_exceptions as exceptions
from src.main_chat.chatbot_manager import ChatbotManager


def main():

    chatbot_manager = ChatbotManager(general_chatbot='Bolek', university_chatbot='Lolek')
    chatbot_manager.create_chatbots()
    while True:
        user_input = input('>>>')
        res = chatbot_manager.ask_chatbot(user_input)
        print('Answer = ', res)

    # initialize_database.init_database()
    # bot.run_bot()

    db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
    # out1 = db.add_conversation(text="Kubica", tag1="agh", tag2="sportowiec", tag3="formuła1")
    # out2 = db.add_conversation(text="Orlen", tag1="agh", tag2="sportowiec", tag3="sponsor")
    # print("Newly added conversations: ", out1, " and ", out2)
    # res = db.get_responses_list_by_tags(tag1="agh", tag2="sportowiec")
    # print("Before update = tag1 = agh, tag2 = sportowiec, text = ", res[0], ", ", res[1])
    # updated_statements = []
    # try:
    #     updated_statements = db.update_conversation_text("Orlen jest sponsorem Kubicy", tag1="agh", tag2="sportowiec")
    # except exceptions.ResponseTextByTagsNotFoundError:
    #     print("No element found for update")
    # updated = db.get_responses_list_by_tags(tag1="agh", tag2="sportowiec")
    # for idx, up in enumerate(updated_statements):
    #     print("After update = tag1 = agh, tag2 = sportowiec, updated text = ", updated[idx], " == up = ", up)
    # print()
    # try:
    #     db.printDocumentsByTags(tag1="agh", tag2="sportowiec")
    # except exceptions.ResponseTextByTagsNotFoundError:
    #     print("Elements matching given tags not found")
    # removed1 = db.remove_conversation(tag1="agh", tag2="sportowiec", tag3="formuła1")
    # removed2 = db.remove_conversation(tag1="agh", tag2="sportowiec", tag3="sponsor")
    # print("Removed conversations text = ", removed1, ", ", removed2)
    #
    # try:
    #     db.create_new_collection('stemming1')
    # except exceptions.CollectionAlreadyExistsInDatabaseError:
    #     db.remove_collection('stemming1')
    #     db.create_new_collection('stemming1')
    #     print("Collection Already Exists Error")
    # try:
    #     docs_to_add = [{'text': 'Mercedes', 'waznosc': 0.9},
    #                                                     {'text': 'Ferrari', 'waznosc': 1.0}]
    #     db.add_doc_with_tags_list('stemming1', ['Renault', 'Red Bull'], "Zespoły F1")
    #     db.add_many_new_docs_to_collection('stemming1', docs_to_add)
    #     print('Before updating in stemming: ', db.get_docs_from_collection('stemming1', {'text': {'$in': ['Renault']}}))
    #     print('Docs filtered with tags list: ', db.get_docs_from_collection_by_tags_list('stemming1', ['Red Bull']))
    #     db.update_many_docs_in_collection('stemming1', {'waznosc': {'$lt': 0.8} }, {'text': 'McLaren', 'waznosc': 0.4})
    #     print('After updating in stemming: ', db.get_docs_from_collection('stemming1', {'text': 'McLaren'}))
    #     print('All docs in stemming: ', list(db.collections_db['stemming1'].find()))
    #     db.remove_collection('stemming1')
    #     print()
    #
    #     db.add_new_doc_to_collection('stop_words', text='Kot',waznosc=0.3)
    #     print("After adding = ", db.get_docs_from_collection('stop_words', {'text': 'Kot' ,'waznosc': 0.3}))
    #     db.update_doc_in_collection('stop_words', {'text': 'Kot', 'waznosc': 0.3}, {'text': 'Kubica', 'waznosc': 1.1} )
    #     print('After update: ', db.get_docs_from_collection('stop_words', {'text': 'Kubica'}))
    #     db.remove_doc_from_collection('stop_words', text='Kubica')
    #     print('After remove: ', db.get_docs_from_collection('stop_words', {'text':'Kubica', 'waznosc': 1.1}))
    # except exceptions.CollectionNotExistsInDatabaseError:
    #     print("Collection Not Exists Error")

    # db.remove_collection('agh_tags_from_response')
    # db.create_new_collection('agh_tags_from_response')
    # db.add_doc_with_tags_list('agh_tags', ['agh', 'wydział'], "Na AGH jest 20 wydziałów")
    # db.add_doc_with_tags_list('agh_tags', ['agh', 'wydział', 'najlepszy'], "Na AGH jest 20 wydziałów i jeden najlepszy")
    # db.add_doc_with_tags_list('agh_tags', ['agh'], "AGH rulez")

    # db.add_doc_with_tags_list('agh_tags_from_response', ['budynek', 'kierunek', 'piękny'], "Na AGH jest 20 budynków")
    # db.add_doc_with_tags_list('agh_tags_from_response', ['budynek', 'kierunek', 'piękny', 'najlepszy'], "Na AGH jest 20 wydziałów i jeden najlepszy budynek")
    # db.add_doc_with_tags_list('agh_tags_from_response', ['budynek'], "AGH rulez budynek")


if __name__ == '__main__':
    main()
