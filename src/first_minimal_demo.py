# -*- coding: utf-8 -*-

import random
import speech_recognition as speech
from gtts import gTTS
import playsound
import os

language = "PL"


def get_category_name(string):
    return string.split(":", 1)[0]


def get_category(user_input):
    user_input_in_quotes = '"' + user_input + '"'
    with open("categories", 'r', encoding='utf-8') as categories:
        for line in categories:
            if user_input_in_quotes in line:
                # print(line)
                # print(get_category_name(line))
                return get_category_name(line)
    return None


def get_possible_category_responses(line):
    possible_responses = line.split("{", 1)[1]
    possible_responses = possible_responses.split("}", 1)[0]
    possible_responses = possible_responses.split(",")
    return possible_responses


def get_response_category(category):
    exact_category = category + ':'
    # print(exact_category)
    with open("category_response", 'r', encoding='utf-8') as category_response:
        for line in category_response:
            if line.startswith(exact_category):
                possible_category_responses = get_possible_category_responses(line)
                choosen_number = random.randint(0, len(possible_category_responses) - 1)
                # print(possible_category_responses[choosen_number])
                return possible_category_responses[choosen_number]


def get_possible_responses(line):
    language_markup = language + '-'
    possible_responses = line.split(language_markup)[1].split(';')[0]
    possible_responses = possible_responses.split(',')
    for i in range(0, len(possible_responses)):
        resp = possible_responses[i]
        possible_responses[i] = resp[1:-1]
    return possible_responses


def get_sample_response(category):
    exact_category = category + ':'
    with open("categories", 'r', encoding='utf-8') as categories:
        for line in categories:
            if line.startswith(exact_category):
                possible_responses = get_possible_responses(line)
                choosen_number = random.randint(0, len(possible_responses) - 1)
                return possible_responses[choosen_number]
    return None


def get_response(user_input):
    user_input = user_input.lower()
    category = get_category(user_input)
    if category is None:
        return None
    response_category = get_response_category(category)
    return get_sample_response(response_category)


def get_default_response():
    if language == 'PL':
        return "Nie wiem jak Ci odpowiedzieć"
    elif language == 'EN':
        return "I do not know what to say"


def calibrate_recognizer(noise_duration, recognizer, source):
    print(f"Please wait for {noise_duration} sec. Calibrating your mic.",
          flush=True)
    recognizer.adjust_for_ambient_noise(source, duration=noise_duration)
    print("Now you can start speaking!", flush=True)


def speech_recognizer(speech_language='pl-PL'):
    r = speech.Recognizer()
    with speech.Microphone() as source:
        audio = r.listen(source)
        print('Plik nagrany. Wysyłanie do rozpoznania')
    try:
        return r.recognize_google(audio, language=speech_language)
    except speech.UnknownValueError:
        return "repeat"
    except speech.RequestError as e:
        return None



def startSpeechRecognition():
    # tts = gTTS('dzień dobry', lang='pl')
    # tts.save('sound.mp3')
    # playsound.playsound('sound.mp3', True)
    r = speech.Recognizer()
    with speech.Microphone() as source:
        calibrate_recognizer(2, r, source)
        while True:
            user_input = speech_recognizer()
            print(user_input)
            resp = get_response(str(user_input))
            if resp != None:
                print(resp)
            else:
                print(get_default_response())


def main():
    r = speech.Recognizer()
    with speech.Microphone() as source:
        calibrate_recognizer(2, r, source)
        i = 0
        while True:
            filename = 'sound' + str(i) + '.mp3'
            user_input = speech_recognizer()
            print(user_input)
            resp = get_response(str(user_input))
            if resp != None:
                tts = gTTS(resp, lang=language)
            else:
                tts = gTTS(get_default_response(), lang=language)
            tts.save(filename)
            playsound.playsound(filename, True)
            os.remove(filename)
            i += 1


main()