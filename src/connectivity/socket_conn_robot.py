# -*- coding: utf-8 -*-


"""
 python2 -m  pip install --user SpeechRecognition
 This file should be run with Python 2

 Goals of methods which are in this file:
    -> tell out response
    -> send text recognized from Pepper to bot
"""
import socket
import sys
from time import sleep
import qi

import speech_recognition as speech


class DataExchangeModule(object):
    def __init__(self, address, port, tts):
        self.data_socket = self.establish_connection(address, port)
        self.tts = tts

    def establish_connection(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            return s
        except socket.error:
            print('Error: connection to ' + host + ':' + str(port) + ' failed, reconnection...')
            sleep(1)
            return self.establish_connection(host, port)

    def send_data_and_tell_response(self, data):
        """
            send data via socket
        """
        try:
            self.data_socket.sendall(bytes(data))
            response = self.data_socket.recv(1024).decode('utf-8')
            if response != '':
                tell(response)
        except socket.error:
            return None

    def tell(self, text):
        """
            cause Pepper say `text`
        """
        self.tts.setLanguage("Polish")
        self.tts.say(text)

    def perform_communication_with_chatbot(self):
        while True:
            print('in loop...')
            result_of_speech_recognition = self.speech_recognizer()
            print("recognized:  " + result_of_speech_recognition + ";")
            send_result = None
            while send_result is None:
                send_result = send_data(self.chatbot_socket, result_of_speech_recognition)
            if send_result != '':
                print(send_result)
