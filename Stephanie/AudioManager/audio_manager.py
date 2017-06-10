from Stephanie.AudioManager.audio_getter import AudioGetter
from Stephanie.AudioManager.audio_recognizer import AudioRecognizer
from Stephanie.configurer import config


class AudioManager:
    def __init__(self, recognizer, UnknownValueError, RequestError):
        self.audio_getter = AudioGetter(recognizer)
        self.audio_recognizer = AudioRecognizer(recognizer, UnknownValueError, RequestError)
        self.c = config

    def get_audio(self, source, signals=True):
        audio = self.audio_getter.get_audio_from_inbuilt(source, signals)
        return audio

    def get_text_from_speech(self, audio):
        option = self.c.config['STT']['master_stt_engine'].lower()
        if option == "bing":
            text = self.audio_recognizer.recognize_from_bing(audio)
            return text
        elif option == "google":
            text = self.audio_recognizer.recognize_from_google(audio)
            return text
        elif option == "google_cloud":
            text = self.audio_recognizer.recognize_from_google_cloud(audio)
            return text
        elif option == "houndify":
            text = self.audio_recognizer.recognize_from_houndify(audio)
            return text
        elif option == "ibm":
            text = self.audio_recognizer.recognize_from_ibm(audio)
            return text
        elif option == "wit":
            text = self.audio_recognizer.recognize_from_wit(audio)
            return text
        else:
            raise Exception("Man, did you mess up with master_stt_engine setting? Yes you did, don't lie to me"
                            "Go check back the docs to see which options we offer, Sigh, tomorrow you'd"
                            "be asking a porche out of internet.")

    def get_text_from_speech_through_google(self, audio):
        option = self.c.config['STT']['initial_stt_engine'].lower()
        if option == "bing":
            text = self.audio_recognizer.recognize_from_bing(audio)
            return text
        elif option == "google":
            text = self.audio_recognizer.recognize_from_google(audio)
            return text
        elif option == "google_cloud":
            text = self.audio_recognizer.recognize_from_google_cloud(audio)
            return text
        elif option == "houndify":
            text = self.audio_recognizer.recognize_from_houndify(audio)
            return text
        elif option == "ibm":
            text = self.audio_recognizer.recognize_from_ibm(audio)
            return text
        elif option == "wit":
            text = self.audio_recognizer.recognize_from_wit(audio)
            return text
        else:
            raise Exception("Man, did you mess up with initial_stt_engine setting? Yes you did, don't lie to me"
                            "Go check back the docs to see which options we offer, Sigh, tomorrow you'd"
                            "be asking a porche out of internet.")
