import os
from gtts import gTTS
from Stephanie.configurer import config


class TextRecognizer:

    def __init__(self):
        self.tts = None
        self.c = config
        self.speech_filename = self.c.config['CORE']['speech_filename']
        self.speech_directory = self.c.config['CORE']['speech_directory']
        self.speech_result_filename = ""

    def recognize_from_google(self, text):
        try:
            self.tts = gTTS(text=text, lang='en')
            return True
        except Exception:
            raise Exception

    def save_speech_from_google(self):
        self.speech_result_filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                   os.pardir,
                                                                   self.speech_directory,
                                                                   self.speech_filename))
        self.tts.save(self.speech_result_filename)
        return self.speech_result_filename
