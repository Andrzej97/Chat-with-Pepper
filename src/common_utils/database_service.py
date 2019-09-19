from chatterbot.storage import MongoDatabaseAdapter
from src.common_utils.custom_exceptions import ResponseTextByTagsNotFoundError
from pymongo import MongoClient
import random

class DatabaseProxy:
    # 'mongodb://localhost:27017/PepperChatDB'
    def __init__(self, conection_uri, database_name):
        self.database_uri = conection_uri + database_name
        self.stat_collection = MongoDatabaseAdapter(database_uri=self.database_uri)
        mongo_client = MongoClient(conection_uri)
        self.collections_db = mongo_client[database_name]

    def is_invalid_arg(self, arg):
        return arg is None

    def add_conversation(self, **tags): # tags == kwargs
        '''Method adds new conversation to database with specified tags
           Returns text of added conversation's statement'''
        try:
            tags.get('text')
        except KeyError:
            print("No \'text\' atribute in **tags in add_conversation()")
            return None
        created_statement = self.stat_collection.create(**tags)
        return created_statement.text

    def get_responses_list_by_tags(self, **tags):
        '''Method returns list of statements text list which match given tags'''
        statement_results = list(self.stat_collection.filter(**tags))
        if len(statement_results) == 0:
            raise ResponseTextByTagsNotFoundError
        text_results = []
        for statement in statement_results:
            text_results.append(statement.text)
        return text_results

    def get_first_response_by_tags(self, **tags):
        '''Method returns first statement's text which match given tags'''
        try:
            responses = self.get_responses_list_by_tags(**tags)
        except ResponseTextByTagsNotFoundError:
            print("No response text for given tags found")
            return None
        return responses[0]

    def get_random_response_by_tags(self, **tags):
        '''Method returns random statement's text which match given tags'''
        try:
            responses = self.get_responses_list_by_tags(**tags)
        except ResponseTextByTagsNotFoundError:
            print("No response text for given tags found")
            return None
        num_of_responses = len(responses)
        index = random.randint(0, num_of_responses)
        return responses[index]

    def remove_conversation(self, **tags):
        '''Method removes conversation specified with tags from database
           It returns text of statement which is removed'''
        conversation_to_remove = self.get_first_response_by_tags(**tags)
        if self.is_invalid_arg(conversation_to_remove):
            return None
        self.stat_collection.remove(conversation_to_remove)
        return conversation_to_remove

    def update_conversation_text(self, new_text, **tags):
        '''Method updates text of statement in database with specified tags
           Returns updated statement's text'''
        matching_statements = list(self.stat_collection.filter(**tags))
        if len(matching_statements) == 0:
            raise ResponseTextByTagsNotFoundError
        updated_statements = []
        for matching_statement in matching_statements:
            matching_statement.text = new_text
            st = self.stat_collection.update(matching_statement)
            updated_statements.append(st.text)
        return updated_statements

    def getCount(self):
        '''Method returns number of documents in database'''
        return self.stat_collection.count()

    def printDocumentsByTags(self, **tags):
        '''Method prints documents from database with specified tags'''
        result_list = list(self.stat_collection.filter(**tags))
        if len(result_list) == 0:
            raise ResponseTextByTagsNotFoundError
        for result in result_list:
            print("Document nr ", result.id, ", text = ", result.text)


    # part of code for collections another than statements
    def add_new_doc_to_collection(self, collection_name, **doc):
        collection = self.collections_db[collection_name]
        collection.insert_one(doc)

    def get_doc_from_collection(self,collection_name, **doc):
        collection = self.collections_db[collection_name]
        docs_found = list(collection.find(doc))
        for d in docs_found:
            print("Doc = ", d)
        return docs_found

    def remove_doc_from_collection(self, collection_name, **doc):
        collection = self.collections_db[collection_name]
        collection.delete_one(doc)

    def update_doc_in_collection(self,collection_name, search_values, new_values):
        collection = self.collections_db[collection_name]
        values_to_update = {"$set": new_values}
        collection.update_one(search_values, values_to_update)