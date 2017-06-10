from Stephanie.configurer import config


# noinspection SpellCheckingInspection
class AudioRecognizer:
    def __init__(self, recognizer, UnknownValueError, RequestError):
        self.UnknownValueError = UnknownValueError
        self.RequestError = RequestError
        self.r = recognizer
        self.c = config

    def recognize_from_sphinx(self, audio):
        # recognize speech using Sphinx
        try:
            text = self.r.recognize_sphinx(audio)
            print("Sphinx thinks you said " + text)
            return text
        except self.UnknownValueError:
            print("Sphinx could not understand audio")
            return False
        except self.RequestError as e:
            print("Sphinx error; {0}".format(e))
            return False

    def recognize_from_google(self, audio):
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = self.r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + text)
            return text
        except KeyError:
            print("Google Recognition couldn't understand your audio with enough confidence.")
        except self.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return False
        except self.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return False

    def recognize_from_google_cloud(self, audio):
        # recognize speech using Google Cloud Speech
        try:
            google_cloud_speech_credentials = self.c.config['STT_KEYS']['google_cloud_speech_api']
        except KeyError:
            print("Api key not found in the config.ini file.")
            return False
        try:
            text = self.r.recognize_google_cloud(audio,
                                                 credentials_json=google_cloud_speech_credentials)
            print("Google Cloud Speech thinks you said " + text)
            return text
        except self.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
            return False
        except self.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))
            return False

    def recognize_from_wit(self, audio):
        # recognize speech using Wit.ai
        try:
            wit_ai_key = self.c.config['STT_KEYS'][
                'wit.ai_speech_api']  # Wit.ai keys are 32-character uppercase alphanumeric strings
        except KeyError:
            print("Api key not found in the config.ini file.")
            return False
        try:
            text = self.r.recognize_wit(audio, key=wit_ai_key)
            print("Wit.ai thinks you said " + text)
            return text
        except self.UnknownValueError:
            print("Wit.ai could not understand audio")
            return False
        except self.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))
            return False

    def recognize_from_bing(self, audio):
        # recognize speech using Microsoft Bing Voice Recognition
        # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
        try:
            bing_key = self.c.config['STT_KEYS']['bing_speech_api']
        except KeyError:
            print("Api key not found in the config.ini file.")
            return False
        try:
            text = self.r.recognize_bing(audio, key=bing_key)
            print("Microsoft Bing Voice Recognition thinks you said " + text)
            return text
        except self.UnknownValueError:
            print("Microsoft Bing Voice Recognition could not understand audio")
            return False
        except self.RequestError as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
            return False

    def recognize_from_houndify(self, audio):
        # recognize speech using Houndify
        try:
            houndify_client_id = self.c.config['STT_KEYS'][
                'houndify_client_id']  # Houndify client IDs are Base64-encoded strings
            houndify_client_key = self.c.config['STT_KEYS'][
                'houndify_client_key']  # Houndify client keys are Base64-encoded strings
        except KeyError:
            print("Api key not found in the config.ini file.")
            return False
        try:
            text = self.r.recognize_houndify(audio, client_id=houndify_client_id,
                                             client_key=houndify_client_key)
            print("Houndify thinks you said " + text)
            return text
        except self.UnknownValueError:
            print("Houndify could not understand audio")
            return False
        except self.RequestError as e:
            print("Could not request results from Houndify service; {0}".format(e))
            return False

    def recognize_from_ibm(self, audio):
        # recognize speech using IBM Speech to Text
        try:
            # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
            ibm_username = self.c.config['STT_KEYS']['ibm_username']
            # IBM Speech to Text passwords are mixed-case alphanumeric strings
            ibm_password = self.c.config['STT_KEYS']['ibm_password']
        except KeyError:
            print("Api key not found in the config.ini file.")
            return False
        try:
            text = self.r.recognize_ibm(audio, username=ibm_username,
                                        password=ibm_password)
            print("IBM Speech to Text thinks you said " + text)
            return text
        except self.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
            return False
        except self.RequestError as e:
            print("Could not request results from IBM Speech to Text service; {0}".format(e))
            return False
