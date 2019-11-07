"""

Code in this file provides server functionality which receives user input as bytes of text via socket connection.
It tries to reach response form `ChatbotManager` and than, sends it back to client.

"""

import socket
import sys

import src.main_chat.chatbot_manager
from configuration import Configuration
from src.common_utils.database.database_service import DatabaseProxy

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9999  # Port to listen on (non-privileged ports are > 1023)


def get_response_from_console(input_statement):
    print("User question: ", input_statement)
    user_input = input("Your response >>>")
    return user_input


class ResponseProvider:
    def __init__(self, is_response_from_console_enabled):
        self.db = DatabaseProxy(Configuration.DATABASE_ADDRESS.value, Configuration.DATABASE_NAME.value)
        self.chatbot_manager = src.main_chat.chatbot_manager.ChatbotManager(intro_chatbot='Bolek',
                                                                            university_chatbot='Lolek',
                                                                            database=self.db)
        self.is_response_from_console_enabled = is_response_from_console_enabled

    def response_source(self, input_statement):
        if not self.is_response_from_console_enabled:
            return self.chatbot_manager.ask_chatbot(input_statement)
        return get_response_from_console(input_statement)

    def receive_and_process(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, Configuration.ROBOT_SOCKET_PORT.value))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024).decode("utf-8")
                    if data:
                        print('received: ' + data)
                        result = self.response_source(data)
                        self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value, response=result)
                        res = bytes(result, "utf-8")
                        conn.sendall(res)


if __name__ == '__main__':
    is_response_from_console_enabled = False
    if len(sys.argv) > 1:
        if sys.argv[1] == '-c' or sys.argv[1] == '--console':
            is_response_from_console_enabled = True
    response_provider = ResponseProvider(is_response_from_console_enabled)
    response_provider.receive_and_process()
