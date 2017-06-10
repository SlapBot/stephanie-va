import re
import speech_recognition as sr
from Stephanie.AudioManager.audio_manager import AudioManager
from Stephanie.TextManager.text_manager import TextManager
from Stephanie.TextProcessor.text_sorter import TextSorter
from Stephanie.TextProcessor.text_learner import TextLearner


class AudioTextManager(AudioManager, TextManager):
    def __init__(self, events):
        self.modules = ()
        self.events = events
        self.r = self.get_recognizer()
        self.sr = self.get_speech_recognition()
        AudioManager.__init__(self, self.r, self.sr.UnknownValueError, self.sr.RequestError)
        TextManager.__init__(self)
        self.sorter = TextSorter()
        self.learner = TextLearner()
        self.audio = None

    def listen(self):
        self.audio = self.process_listen()
        return self

    def hear(self, source):
        audio = self.get_audio(source)
        return audio

    def decipher(self):
        text = self.get_text_from_speech(self.audio)
        return text

    def say(self, speech):
        speech_result_filename = self.get_speech_from_text(speech).save_speech_result()
        self.speak_result(speech_result_filename)

    def understand(self, modules, raw_text, explicit=False):
        module_info = self.set_modules(modules).learn(raw_text, explicit)
        return self.get_method_name(module_info['module_info'])

    def set_modules(self, modules):
        self.modules = modules
        return self

    def sort(self, raw_text, explicit):
        if raw_text:
            subwords, keywords = self.sorter.sort(raw_text, explicit)
            return subwords, keywords
        return False, False

    def learn(self, raw_text, explicit=False):
        subwords, keywords = self.sort(raw_text, explicit)
        if keywords:
            module_info = self.learner.set_modules(self.modules).learn(keywords)
            print(module_info)
            return {
                'subwords': subwords,
                'keywords': keywords,
                'module_info': module_info
            }
        else:
            return False

    @staticmethod
    def get_recognizer():
        return sr.Recognizer()

    @staticmethod
    def get_speech_recognition():
        return sr

    def process_listen(self):
        with self.sr.Microphone() as source:
            return self.hear(source)

    def get_method_name(self, module_info):
        raw_func_name = module_info[0].split("@")[1]
        func_name = self.convert_to_snake_case(raw_func_name)
        return func_name

    @staticmethod
    def convert_to_snake_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
