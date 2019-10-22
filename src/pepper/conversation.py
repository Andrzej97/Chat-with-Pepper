from naoqi import AlProxy
#
def tell_response(text):
    tts = ALProxy("ALTextToSpeech", "192.168.1.101", 9559)
    tts.setLanguage("Polish")
    tts.say(text)

import sys
print("\n".join(sys.path))