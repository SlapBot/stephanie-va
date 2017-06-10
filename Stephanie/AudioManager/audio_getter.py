import os
from Stephanie.configurer import config
from Stephanie.TextManager.speaker import Speaker


class AudioGetter:
    def __init__(self, recognizer):
        self.r = recognizer
        self.c = config
        self.speaker = Speaker()
        self.start_text = self.c.config['LOGS']['start_text']
        self.listened_success_text = self.c.config['LOGS']['listened_success_text']
        self.listened_error_text = self.c.config['LOGS']['listened_error_text']
        self.speech_directory = self.c.config['CORE']['speech_directory']
        self.beep_start = self.get_speeches_folder(self.c.config['CORE']['beep_start'])
        self.beep_end = self.get_speeches_folder(self.c.config['CORE']['beep_end'])

    def get_audio_from_inbuilt(self, source, signals=True):
        print(self.start_text)
        try:
            if signals:
                self.speaker.speak_from_os(self.beep_start)
            self.r.adjust_for_ambient_noise(source, duration=1)
            audio = self.r.listen(source)
            print(self.listened_success_text)
            if signals:
                self.speaker.speak_from_os(self.beep_end)
            return audio
        except AssertionError:
            print(self.listened_error_text)
            return False

    def listen(self, source, signals=True):
        try:
            self.get_audio_from_inbuilt(source, signals)
        except:
            raise Exception("Make sure some kind of speaking device is properly installed in your system.")

    def get_speeches_folder(self, filename):
        return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir,
                                            self.speech_directory,
                                            filename))
