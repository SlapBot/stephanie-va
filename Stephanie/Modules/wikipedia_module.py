from urllib.request import Request, urlopen
from urllib.error import URLError
import json
from Stephanie.Modules.base_module import BaseModule


class WikipediaModule(BaseModule):
    def __init__(self, *args):
        super(WikipediaModule, self).__init__(*args)

    def give_a_summary(self):
        self.assistant.say("What would you like to know about?")
        text = self.assistant.listen().decipher()
        text = text.strip().replace(" ", "%20")
        request = Request(
            'https://en.wikipedia.org/w/api.php?'
            'format=json&action=query&prop=extracts&exintro=&explaintext=&titles=' + text
        )
        try:
            response = urlopen(request)
            data = json.loads(
                response.read().decode(
                    response.info().get_param('charset') or 'utf-8'
                )
            )
            output = data["query"]["pages"]
            final = output[list(output.keys())[0]]["extract"]
            return final

        except URLError:
            return "Unable to search your given query."
