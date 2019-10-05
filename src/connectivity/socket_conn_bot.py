"""

Code in this file provides server functionality which receives user input as bytes of text via socket connection.
It tries to reach response form `ChatbotManager` and than, sends it back to client.

"""

import socket
from src.main_chat.chatbot_manager import ChatbotManager

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

chatbot_manager = ChatbotManager(intro_chatbot='Bolek', university_chatbot='Lolek',
                                 connection_uri='mongodb://localhost:27017/', database_name='PepperChatDB')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024).decode("utf-8")
            if data:
                result = chatbot_manager.ask_chatbot(data)
                res = bytes(result, "utf-8")
                conn.sendall(res)
