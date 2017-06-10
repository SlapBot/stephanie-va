from Stephanie.Modules.base_module import BaseModule
from Stephanie.local_libs.pymato import Pymato
import webbrowser


class ZomatoModule(BaseModule):
    def __init__(self, *args):
        super(ZomatoModule, self).__init__(*args)
        self.api_key = self.get_configuration("zomato_api_key")
        if self.api_key:
            self.z = Pymato(self.api_key)
        else:
            return False
        self.city = self.get_configuration(section="USER", key="city")

    def handle(self):
        status = self.z.set_location(self.city)
        if not status:
            return "Your api key wasn't provided or maybe your city isn't available."
        rests = self.z.get_location_details()
        if not rests:
            return "No good places to eat found nearby your location."
        for rest in rests:
            rest = rest['restaurant']
            self.assistant.say("%s situated nearby %s is found, it offers cuisines like %s "
                               "with an average price range of %s %s per person, and over %s people have"
                               "rated this place with an average ratings as %s. "
                               "So would you like to order this place?"
                               % (
                                   rest['name'],
                                   rest['location']['locality'],
                                   rest['cuisines'],
                                   rest['currency'],
                                   round(rest['average_cost_for_two'] / 2),
                                   rest['user_rating']['votes'],
                                   rest['user_rating']['aggregate_rating']
                               ))
            text = self.assistant.listen().decipher()
            if text.upper() in self.AFFIRMATIVE:
                webbrowser.open(rest['url'])
                return "Thank you."
            self.assistant.say("okay, then how about this one? ")
        return "That's all the restaurants available near your location."
