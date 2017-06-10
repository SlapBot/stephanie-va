from Stephanie.Modules.base_module import BaseModule
from Stephanie.local_libs.wolframalpha_speech.index import WolframalphaSpeech
from Stephanie.local_libs.wolframalpha_speech.exceptions_manager import *


class AlphaSearchModule(BaseModule):
    def __init__(self, *args):
        super(AlphaSearchModule, self).__init__(*args)
        self.app_id = self.get_configuration('wolframalpha_search_engine_key')
        if self.app_id:
            self.client = WolframalphaSpeech(self.app_id)
        else:
            return False

    def do_a_search(self):
        status = False
        phrase = ""
        raw_text_array = self.raw_text.split()
        end_index = len(raw_text_array)
        for i in range(0, end_index):
            if status:
                phrase += " " + raw_text_array[i]
            elif raw_text_array[i] == "search":
                status = True
        if status is False:
            return "Can you possibly phrase it a bit better?"
        phrase = phrase.strip()
        try:
            text = self.client.search(phrase)
        except ConfidenceError:
            return "Sorry, I couldn't find what you asked for, maybe try being a little more specific."
        except InternalError:
            return "It seems something is wrong with the wolframalpha search engine, maybe try asking later."
        except MissingTokenError:
            return "Seems you haven't provided the API TOKEN for search engine, please add it in config file."
            print("API TOKEN for wolframalpha search engine is missing, head in to docs to see how to properly fill the configurations for search engine.")
        except InvalidTokenError:
            return "Seems you haven't provided the API TOKEN or it's wrong for search engine, please add it in config file."
            print("API TOKEN for wolframalpha search engine is missing or is invalid, head in to docs to see how to properly fill the configurations for search engine.")
        return text
