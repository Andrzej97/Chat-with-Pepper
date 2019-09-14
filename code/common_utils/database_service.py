from chatterbot.storage import MongoDatabaseAdapter
import random

# remember to add errors handling
class DatabaseProxy:
    db = MongoDatabaseAdapter(database_uri='mongodb://localhost:27017/PepperChatDB')

    # def testing_create(self):
    #     self.db.create(text="test_tworzenia", conversation="testowanie", my_tag="moj_tag")

    def add_conversation(self, **tags): # tags == kwargs
        created_statement = self.db.create(**tags)
        return created_statement.text

    def get_responses_list_by_tags(self, **tags):
        statement_results = list(self.db.filter(**tags))
        text_results = []
        for statement in statement_results:
            text_results.append(statement.text)
        return text_results

    def get_first_response_by_tags(self, **tags):
        responses = self.get_responses_list_by_tags(**tags)
        return responses[0]

    def get_random_response_by_tags(self, **tags):
        responses = self.get_responses_list_by_tags(**tags)
        num_of_responses = len(responses)
        index = random.randint(0, num_of_responses)
        return responses[index]

    def remove_conversation(self, **tags):
        conversation_to_remove = self.get_first_response_by_tags(**tags)
        self.db.remove(conversation_to_remove)
        return conversation_to_remove


    def getCount(self):
        return self.db.count()
