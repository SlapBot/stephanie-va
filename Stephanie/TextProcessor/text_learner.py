from Stephanie.configurer import config
from sounder import Sounder


class TextLearner:
    def __init__(self):
        self.modules = self.get_modules()
        self.chances = []
        self.searcher = Sounder()

    def set_modules(self, modules):
        self.modules = modules
        return self

    def learn(self, key_words):
        module_func = self.understand(key_words)
        print(module_func)
        return module_func

    @staticmethod
    def get_modules():
        c = config
        return c.get_modules()

    def understand(self, keywords):
        print(keywords)
        dataset = []
        for x in self.modules:
            dataset.append(x[1])
        return self.modules[self.searcher.set_dataset(dataset).search(keywords)]
