from difflib import SequenceMatcher as sm
from metaphone import doublemetaphone as dm
from Stephanie.configurer import config


class TextSorter:
    def __init__(self):
        self.raw_text_array = []
        self.sub_words = []
        self.key_words = []
        self.reserved_sub_words = self.get_reserved_sub_words()
        self.c = config

    def sort(self, raw_text, explicit=True):
        return self.clean(raw_text, explicit).process()

    def clean(self, raw_text, explicit):
        raw_text = raw_text.lower()
        self.raw_text_array = raw_text.split()
        if explicit:
            self.greet_engine()
        self.key_words = self.raw_text_array.copy()
        return self

    def process(self):
        for index, raw_text in enumerate(self.raw_text_array):
            if raw_text in self.reserved_sub_words:
                self.sub_words.append(raw_text)
                self.key_words.remove(raw_text)
        return self.sub_words, self.key_words

    @staticmethod
    def get_reserved_sub_words():
        return {
            "what", "where", "which", "how", "when", "who",
            "is", "are", "makes", "made", "make", "did", "do",
            "to", "the", "of", "from", "against", "and", "or",
            "you", "me", "we", "us", "your", "my", "mine", 'yours',
            "could", "would", "may", "might", "let", "possibly",
            'tell', "give", "told", "gave", "know", "knew",
            'a', 'am', 'an', 'i', 'like', 'has', 'have', 'need',
            'will', 'be', "this", 'that', "for"
        }

    def greet_engine(self):
        assistant_name = self.c.config.get('SYSTEM', 'assistant_name')
        meta_name = dm(assistant_name)[0]
        for index, raw_text in enumerate(self.raw_text_array):
            meta_text = dm(raw_text)[0]
            chances = sm(None, meta_name, meta_text).ratio()
            if chances > 0.7:
                self.raw_text_array = self.raw_text_array[index+1:]
                return
