from newsapi.articles import Articles
from newsapi.sources import Sources


class Reporter:
    def __init__(self, API_KEY):
        self.articles = Articles(API_KEY)
        self.sources = Sources(API_KEY)
        self.sources.information()

    def get_all_categories(self):
        categories = list(self.sources.all_categories())
        return categories

    def get_all_categories(self):
        categories = list(self.sources.all_categories())
        return categories
