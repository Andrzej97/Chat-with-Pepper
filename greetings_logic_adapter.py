from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter


class GreetingAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        statement.text = statement.text.lower()
        db = SQLStorageAdapter()
        words = db.filter(conversation='greeting')
        for w in words:
            if w.text == statement.text:
                return True
        return False

    def process(self, statement, additional_respones_parameters):
        import random
        from chatterbot.conversation import Statement

        words = SQLStorageAdapter().filter(conversation='greeting')
        words_list = []
        for w in words:
            words_list.append(w)

        selected_statement = Statement(statement.text)
        while statement.text == selected_statement.text:
            selected_statement.text = words_list[random.randint(0, len(words_list))].text
        selected_statement.confidence = 1
        return selected_statement
