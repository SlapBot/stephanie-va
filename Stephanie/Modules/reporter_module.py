from Stephanie.Modules.base_module import BaseModule
from newsapi.articles import Articles
from newsapi.sources import Sources


class ReporterModule(BaseModule):
    AFFIRMATIVE = ["YES", "YEAH", "SURE", "YAH", "YA"]
    NEGATIVE = ["NO", "NEGATIVE", "NAH", "NA", "NOPE"]

    def __init__(self, *args):
        super(ReporterModule, self).__init__(*args)
        self.API_KEY = self.get_configuration("newsapi.org_key")
        self.threshold = int(self.get_configuration("news_limit"))
        if self.API_KEY:
            self.articles = Articles(self.API_KEY)
            self.sources = Sources(self.API_KEY)
        else:
            print("Kindly look back at the documentation to configure news module properly especially the API keys.")
            return False
        self.sources_url = {}
        self.sources.information()

    def get_all_categories(self):
        return list(self.sources.all_categories())

    def get_by_category(self, category):
        srcs = self.sources.get_by_category(category).sources
        self.sources_url = {}
        for src in srcs:
            self.sources_url[src['name']] = src['url']
        return self.sources_url

    def get_sort_bys_of_source(self, source_name):
        return self.sources.search(source_name)[0]['sortBysAvailable']

    def all_sources(self):
        self.sources_url = self.sources.all_names()
        return self.sources_url

    def get_news(self):
        self.assistant.say("Would you prefer any specific category? If yes then what would it be?")
        category_status = self.assistant.listen().decipher()
        if category_status.upper() in self.NEGATIVE:
            category = False
        else:
            categories = self.get_all_categories()
            category = self.search(categories, category_status)
        self.assistant.say("Any preference you would like to have about source of your news? like CNN"
                           "or Time magazine or maybe The hindu?")
        source_status = self.assistant.listen().decipher()
        if source_status.upper() in self.NEGATIVE:
            source = False
        else:
            if category:
                sources_available = self.get_by_category(category)
                response = "Out of all the sources as follows"
                for source_name, source_url in sources_available.items():
                    response += " %s," % source_name
                response += ", which one would you like to pick?"
                self.assistant.say(response)
                source_command = self.assistant.listen().decipher()
                source = self.search(list(sources_available), source_command)
            else:
                self.assistant.say("So would you want me to list all the sources around 70 which to be"
                                   "honest would be a hefty task, so if not, then just let me know of"
                                   "your source name and I would let you know if it's available or not.")
                all_sources_status = self.assistant.listen().decipher()
                sources_available = self.all_sources()
                if all_sources_status.upper() in self.AFFIRMATIVE:
                    response = "Good job, lazy ass, so here are all the available sources as follows "
                    sources_available_list = list(sources_available)
                    for source_name in sources_available_list:
                        response += " %s," % source_name
                    response += ", which one would you like to pick?"
                    self.assistant.say(response)
                    source_command = self.assistant.listen().decipher()
                    all_sources_status = source_command
                source_found = self.search(list(sources_available), all_sources_status)
                source = source_found
        if source:
            sort_bys_available = self.get_sort_bys_of_source(source)
            if len(sort_bys_available) == 1:
                sort_by = sort_bys_available[0]
            else:
                if len(sort_bys_available) == 2:
                    response = "And what kind of news sort would you like? " \
                               "%s or %s?" % (sort_bys_available[0], sort_bys_available[1])
                else:
                    response = "And what kind of news sort would you like? " \
                               "%s or %s, or maybe %s?" % (sort_bys_available[0],
                                                           sort_bys_available[1],
                                                           sort_bys_available[2])
                self.assistant.say(response)
                sort_by_command = self.assistant.listen().decipher()
                sort_by = self.search(sort_bys_available, sort_by_command)
        else:
            self.assistant.say("And what kind of news sort would you like?"
                               "latest or maybe top ones shown in front page?")
            sort_status_command = self.assistant.listen().decipher()
            sort_by = self.search(['top', 'popular' 'latest'], sort_status_command)
        if not source:
            if sort_by.lower() == "top":
                source = "google-news"
            elif sort_by.lower() == "latest":
                source = "the-telegraph"
            else:
                source = "time"
        response = self.get_response(source, sort_by)
        return response

    def handle(self):
        source = self.get_configuration("news_source")
        response = self.get_response(source)
        return response

    def get_response(self, source, sort_by=None, threshold=5):
        if self.threshold:
            threshold = self.threshold
        source = source.lower().replace(" ", "-")
        articles = self.articles.get(source, sort_by=sort_by).articles
        articles = articles[:threshold]
        response = "So the %s news from %s news source are as follows " % (sort_by, source)
        for article in articles:
            if article['title']:
                response += "%s, " % article['title']
            if article['description']:
                response += "%s, " % article['description']
            if article['author']:
                response += "was reported by %s." % article['author']
            response += "and in the other news. "
        return response

    @staticmethod
    def search(dataset, query):
        values = [0 for _ in range(0, len(dataset))]
        search = query.lower().split()
        upper_threshold = len(search)
        for index, data in enumerate(dataset):
            search_array = data.split()
            for index2, text in enumerate(search_array):
                if index2 >= upper_threshold:
                    break
                threshold = len(search[index2])
                for i in range(0, len(text)):
                    if i >= threshold - 1:
                        break
                    if text[i] == search[index2][i]:
                        values[index] += 1
        max_value = max(values)
        max_index = values.index(max_value)
        return dataset[max_index]
