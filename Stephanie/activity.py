from Stephanie.local_libs.activity_search import ActivitySearch
from Stephanie.commander import Commander
from Stephanie.configurer import config


class Activity(Commander):
    def __init__(self, speech_recognition, recognizer, events):
        super(Activity, self).__init__(speech_recognition, recognizer, events)
        self.c = config
        self.ass = ActivitySearch()

    def check(self, source):
        audio = self.get_audio(source, signals=False)
        if not audio:
            return audio
        text = self.get_text_from_speech_through_google(audio)
        if not text:
            return text
        status = self.check_for_status(text)
        return status

    def check_for_status(self, text):
        return self.calculate(text)

    def calculate(self, text):
        default_text_array = ['stephanie', 'wake', 'up']
        command_text = self.c.config.get("SYSTEM", "wake_up_command")
        command_text_array = command_text.lower().split()
        user_text_array = text.split()
        chances = self.get_chances(command_text_array, user_text_array)
        if command_text_array == default_text_array:
            chances2 = self.get_chances(['stephanie', 'wakeup'], user_text_array)
            if chances2 > chances:
                chances = chances2
        if chances > 70.0:
            return True
        return False

    def check_always_on(self, source):
        audio = self.get_audio(source, signals=False)
        if not audio:
            return audio
        text = self.get_text_from_speech_through_google(audio)
        if not text:
            return text
        status = self.check_for_status_always_on(text)
        return status

    def check_for_status_always_on(self, text):
        return self.calculate_always_on(text)

    def calculate_always_on(self, text):
        assistant_name = self.c.config.get("SYSTEM", "assistant_name")
        command_text_array = assistant_name.lower().split()
        user_text_array = text.split()
        chances = self.get_chances(command_text_array, user_text_array)
        if chances > 70.0:
            return True
        return False

    def get_chances(self, given_keywords, user_keywords, exact=True):
        chances = self.ass.get_probability(given_keywords=given_keywords,
                                           user_keywords=user_keywords)
        if exact:
            return chances[0]
        return chances
