import speech_recognition as speech

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
        return r.recognize_google(audio, language=speech_language)
    except speech.UnknownValueError:
        return "repeat"
    except speech.RequestError as e:
        return None


def startSpeechRecognition():
    r = speech.Recognizer()
    with speech.Microphone() as source:
        calibrate_recognizer(2, r, source)
        while True:
            cmd = speech_recognizer()
            print(cmd)

startSpeechRecognition()