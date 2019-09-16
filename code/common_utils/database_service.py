from chatterbot.storage import MongoDatabaseAdapter
from code.common_utils.custom_exceptions import ResponseTextByTagsNotFoundError
import random

class DatabaseProxy:
    db = MongoDatabaseAdapter(database_uri='mongodb://localhost:27017/PepperChatDB')

    def is_invalid_arg(self, arg):
        return arg is None

    def add_conversation(self, **tags): # tags == kwargs
        '''Method adds new conversation to database with specified tags
           Returns text of added conversation's statement'''
        try:
            tags.get('name')
        except KeyError:
            print("No \'name\' atribute in **tags in add_conversation()")
            return None
        created_statement = self.db.create(**tags)
        return created_statement.text

    def get_responses_list_by_tags(self, **tags):
        '''Method returns list of statements text list which match given tags'''
        statement_results = list(self.db.filter(**tags))
        if(len(statement_results) == 0):
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
           It returns statement's text which is removed'''
        conversation_to_remove = self.get_first_response_by_tags(**tags)
        if self.is_invalid_arg(conversation_to_remove):
            return None
        self.db.remove(conversation_to_remove)
        return conversation_to_remove

    def update_conversation_text(self, new_text, **tags):
        '''Method updates text of statement in database with specified tags
           Returns updated statement's text'''
        try:
            matching_statement = list(self.db.filter(**tags))[0]
        except IndexError:
            print("No element found for update")
            return None
        matching_statement.text = new_text
        st = self.db.update(matching_statement)
        return st.text

    def getCount(self):
        '''Method returns number of documents in database'''
        return self.db.count()

    def printDocumentsByTags(self, **tags):
        '''Method prints documents from database with specified tags'''
        result_list = list(self.db.filter(**tags))
        for result in result_list:
            print("Document nr ", result.id, " ,text = ", result.text)
