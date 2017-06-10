from Stephanie.commander import Commander


class VirtualAssistant(Commander):
    def __init__(self, speech_recognition, recognizer, events):
        super(VirtualAssistant, self).__init__(speech_recognition, recognizer, events)

    def main(self, source):
        audio = self.get_audio(source)
        if not audio:
            return audio
        text = self.get_text_from_speech(audio)
        if not text:
            return text
        result_text = self.process_text(text)
        if result_text is None:
            return
        speech_filename = self.get_speech_from_text(result_text).save_speech_result()
        self.speak_result(speech_filename)
