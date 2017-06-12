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
        self.tts_option = self.c.config['TTS']['tts_player'].lower()

    def get_audio_from_inbuilt(self, source, signals=True):
        print(self.start_text)
        try:
            if signals:
                if self.tts_option == "os":
                    self.speaker.speak_from_os(self.beep_start)
                elif self.tts_option == "mixer":
                    self.speaker.speak_from_pygame(self.beep_start)
                else:
                    raise AssertionError("Fill in the tts_player option in config.ini file as either os or mixer.")
            self.r.adjust_for_ambient_noise(source, duration=1)
            audio = self.r.listen(source)
            print(self.listened_success_text)
            if signals:
                if self.tts_option == "os":
                    self.speaker.speak_from_os(self.beep_end)
                elif self.tts_option == "mixer":
                    self.speaker.speak_from_pygame(self.beep_end)
                else:
                    raise AssertionError("Fill in the tts_player option in config.ini file as either os or mixer.")
            return audio
        except AssertionError as e:
            print(e)
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
