from Stephanie.AudioManager.audio_manager import AudioManager
from Stephanie.TextProcessor.text_processor import TextProcessor
from Stephanie.TextManager.text_manager import TextManager


class Commander:
    def __init__(self, speech_recognition, recognizer, events):
        self.events = events
        self.audio_manager = AudioManager(recognizer, speech_recognition.UnknownValueError,
                                          speech_recognition.RequestError)
        self.text_processor = TextProcessor(events)
        self.text_manager = TextManager()

    def get_audio(self, source, signals=True):
        audio = self.audio_manager.get_audio(source, signals)
        return audio

    def get_text_from_speech(self, audio):
        text = self.audio_manager.get_text_from_speech(audio)
        return text

    def get_text_from_speech_through_google(self, audio):
        text = self.audio_manager.get_text_from_speech_through_google(audio)
        return text

    def process_text(self, text):
        result_text = self.text_processor.process(text)
        return result_text

    def get_speech_from_text(self, text):
        self.text_manager.get_speech_from_text(text)
        return self

    def save_speech_result(self):
        return self.text_manager.save_speech_result()

    def speak_result(self, speech_result_filename):
        self.text_manager.speak_result(speech_result_filename)
