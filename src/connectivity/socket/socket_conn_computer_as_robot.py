# -*- coding: utf-8 -*-


"""
 python2 -m  pip install --user SpeechRecognition
 This file should be run with Python 2

 Goals of methods which are in this file:
    -> get sound samples from Pepper microphones
    -> send this to google web api, which converts it to text
    -> send text to bot
    -> send response received from bot to Pepper
"""
import socket
import sys
from time import sleep
import qi

import speech_recognition as speech

ROBOT_ADDRESS = "192.168.1.101"
ROBOT_PORT = 9559

BOT_ADDRESS = 'localhost'
BOT_PORT = 65432


def send_data(connection_socket, data):
    """
        send data via socket
    """
    try:
        connection_socket.sendall(bytes(data))
        response = connection_socket.recv(1024).decode('utf-8')
        return response
    except socket.error:
        return None


def tell(tts, text):
    """
        cause Pepper say `text`
    """
    tts.setLanguage("Polish")
    tts.say(text)


class Robot():
    def __init__(self):
        """
        Initialise services and variables.
        """
        reload(sys)
        sys.setdefaultencoding('utf8')  # required for socket communication

        self.speech_recognizer = speech.Recognizer()
        self.rate = 1600  # default rate in Hertz
        self.chatbot_socket = self.establish_connection(BOT_ADDRESS, BOT_PORT)
        # self.tts = ALProxy("ALTextToSpeech", ROBOT_ADDRESS, ROBOT_PORT)  # establish connection with robot
        # above line will cause failures until you are not in the same network with Pepper

    def microphone_speech_recorder(self):
        with speech.Microphone() as source:
            audio = self.speech_recognizer.listen(source)
        return audio

    def start_processing(self):
        """
        Start processing
        """
        # ask for the front microphone signal sampled at 16kHz
        # if you want the 4 channels call setClientPreferences(self.module_name, 48000, 0, 0)
        self.audio_service.setClientPreferences(self.module_name, self.rate, 3, 0)
        self.audio_service.subscribe(self.module_name)

        while not self.isProcessingDone:
            sleep(1)

        self.audio_service.unsubscribe(self.module_name)

    def process_remote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):
        """
        this method is run on sound samples stream from microphone
        """
        audio_data = self.raw_speech_to_audio_data(inputBuffer)
        text = self.speech_to_text(audio_data)

    def raw_speech_to_audio_data(self, raw_data):

        """
        Here width of frame is assumed to be 2 bytes, according to information I found in examples of source code.
        However this value can be not valid, so it should be tested. All possible values according to `AudioData`
        source code is 1-4.
        """
        return speech.AudioData(frame_data=raw_data, sample_rate=self.rate, sample_width=2)

    def speech_to_text(self, audio, speech_language='pl-PL'):
        try:
            result = self.speech_recognizer.recognize_google(audio, language=speech_language)
            print('>>>>>> ' + result)
            return result
        except speech.UnknownValueError:
            return "repeat"
        except speech.RequestError as e:
            return None

    def establish_connection(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            return s
        except socket.error:
            print('Error: connection to ' + host + ':' + str(port) + 'failed, reconnection...')
            sleep(1)
            return self.establish_connection(host, port)

    def perform_communication_with_chatbot(self):
        while True:
            print('in loop...')
            audio = self.microphone_speech_recorder()
            result_of_speech_recognition = self.speech_to_text(audio)
            print("recognized:  " + result_of_speech_recognition + ";")
            if result_of_speech_recognition != 'repeat':
                send_result = None
                while send_result is None:
                    send_result = send_data(self.chatbot_socket, result_of_speech_recognition)
                if send_result != '':
                    print(send_result)
                    # self.tts.tell(tts, send_result)


Robot().perform_communication_with_chatbot()
