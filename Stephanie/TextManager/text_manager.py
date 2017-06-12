from Stephanie.TextManager.text_recognizer import TextRecognizer
from Stephanie.TextManager.speaker import Speaker
from Stephanie.configurer import config


class TextManager:
    def __init__(self):
        self.text_recognizer = TextRecognizer()
        self.speaker = Speaker()
        self.c = config

    def get_speech_from_text(self, text):
        option = self.c.config['TTS']['tts_engine'].lower()
        if option == "google":
            try:
                self.text_recognizer.recognize_from_google(text)
            except:
                print("Some issue with google text to speech mechanism, change to some other service."
                      " Or just wait for some time mate, turning off and on do magic sometimes too.")
            return self
        else:
            raise Exception("Man, did you mess up with tts_engine setting? Yes you did, don't lie to me"
                            "Go check back the docs to see which options we offer, Sigh, tomorrow you'd"
                            "be asking a porche out of internet.")

    def save_speech_result(self):
        try:
            return self.text_recognizer.save_speech_from_google()
        except:
            print("Look it shouldn't happen but since it happened, just get to support tab of main website mate,"
                  " some issue with os is what I assume unless you haven't changed code if in that case"
                  "man, well.")

    def speak_result(self, speech_result_filename):
        option = self.c.config['TTS']['tts_player'].lower()
        if option == "os":
            self.speaker.speak_from_os(speech_result_filename)
        elif option == "mixer":
            self.speaker.speak_from_pygame(speech_result_filename)
        else:
            raise Exception("Man, did you mess up with tts_player setting?\n"
                            "Yes you did, don't lie to me.\n"
                            "Go check back the docs to see which options we offer. It's either os or mixer\n"
                            "Sigh, tomorrow you'd be asking a porche out of internet.")

    def speak(self, text):
        filename = self.get_speech_from_text(text).save_speech_result()
        self.speak_result(filename)
