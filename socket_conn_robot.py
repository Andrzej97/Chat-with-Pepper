#-*- coding: utf-8 -*-
# python2 -m  pip install --user SpeechRecognition
import speech_recognition as speech
from contextlib import closing
from naoqi import ALProxy
import sounddevice as sd
import numpy
import socket

def speech_recognizer(speech_language='pl-PL'):
    r = speech.Recognizer()
    # with speech.Microphone() as source:
    #     audio = r.listen(source)

    r = speech.Recognizer()
    with speech.Microphone() as source:
        audio = r.listen(source)

    try:
        result = r.recognize_google(audio, language=speech_language)
        print('>>>>>> ' + result)
        return result
    except speech.UnknownValueError:
        return "repeat"
    except speech.RequestError as e:
        return None

def tell(text):
    tts = ALProxy("ALTextToSpeech", "192.168.1.101", 9559)
    tts.setLanguage("Polish")
    tts.say(text)

def send_data(data):
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432

    with closing(socket.socket()) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(data))
        data = s.recv(1024)

    print('Received', repr(data))

# speech_recognizer()

# send_data(speech_recognizer())
while True:
    result = speech_recognizer()
    print("recognized:  " + result + ";;")
    send_data(result)
# username: nao, password: 1pepper2

# chatter bot - offline'owa biblioteka