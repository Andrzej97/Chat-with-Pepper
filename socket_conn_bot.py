import socket
from src.main_chat.chatbot_manager import ChatbotManager

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

chatbot_manager = ChatbotManager(general_chatbot='Bolek', university_chatbot='Lolek')
chatbot_manager.create_chatbots()



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data)
            chatbot_manager.ask_chatbot(data)
            # conn.sendall(data)