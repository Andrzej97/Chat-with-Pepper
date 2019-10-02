import speech_recognition as speech

from src.main_chat.chatbot_manager import ChatbotManager


def calibrate_recognizer(noise_duration, recognizer, source):
    print(f"Please wait for {noise_duration} sec. Calibrating your mic.",
          flush=True)
    recognizer.adjust_for_ambient_noise(source, duration=noise_duration)
    print("Now you can start speaking!", flush=True)


def speech_recognizer(speech_language='pl-PL'):
    r = speech.Recognizer()
    with speech.Microphone() as source:
        audio = r.listen(source)
    try:
        result = r.recognize_google(audio, language=speech_language)
        print('>>>>>> ' + result)
        return r.recognize_google(audio, language=speech_language)
    except speech.UnknownValueError:
        return "repeat"
    except speech.RequestError as e:
        return None


def startSpeechRecognition():
    r = speech.Recognizer()
    with speech.Microphone() as source:
        calibrate_recognizer(2, r, source)

        chatbot_manager = ChatbotManager(general_chatbot='Bolek', university_chatbot='Lolek')
        chatbot_manager.create_chatbots()

        while True:
            cmd = speech_recognizer()
            print("resp: " + chatbot_manager.ask_chatbot(cmd))

startSpeechRecognition()
