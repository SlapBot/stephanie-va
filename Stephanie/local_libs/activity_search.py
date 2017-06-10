from sounder import Sounder


class ActivitySearch:
    def __init__(self):
        self.sounder = Sounder()

    def get_probability(self, given_keywords, user_keywords):
        info = self.sounder.probability(query=user_keywords, dataset=given_keywords, 
                                        prediction=True, metaphone=True, detailed=True)
        return info['chances']
