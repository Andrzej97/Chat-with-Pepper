
"""

Code in this file provides server functionality which receives user input as bytes of text via socket connection.
It tries to reach response form `ChatbotManager` and than, sends it back to client.

"""

import socket
# from src.main_chat.chatbot_manager import ChatbotManager
import src.common_utils.constants as constans
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9999  # Port to listen on (non-privileged ports are > 1023)

#chatbot_manager = ChatbotManager(intro_chatbot='Bolek', university_chatbot='Lolek',
 #                                connection_uri='mongodb://localhost:27017/', database_name='PepperChatDB')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print('debug1')
    s.bind((HOST, constans.ROBOT_SOCKET_PORT))
    print('debug2')
    s.listen(16)
    print('debug3')
    conn, addr = s.accept()
    print('debug4')
    with conn:
        while True:
            print('czekam na dane')
            data = conn.recv(1024).decode("utf-8")
            if data:
                print('received: ' + data)
                # result = chatbot_manager.ask_chatbot(data)
                result = 'Nauczono mnie by nie odpowiadac obcym, najpierw sie poznajmy, mam na imie Pepper, a Ty?'
                print(result)
                res = bytes(result, "utf-8")
                conn.sendall(res)
