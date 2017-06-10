class SearchModule:
    def __init__(self):
        pass

    def search_for_competition_by_name(self, competitions, query):
        m, answer = self.search(competitions, attribute_name="caption", query=query)
        if m == 0:
            return False
        return answer

    def search_for_competition_by_code(self, competitions, query):
        return self.search_by_code(competitions, attribute_name="league", query=query)

    def search_for_team_by_name(self, teams, query):
        m, answer = self.search(teams, attribute_name="name", query=query)
        if m == 0:
            return False
        return answer

    def search_for_team_by_code(self, teams, query):
        return self.search_by_code(teams, attribute_name="code", query=query)

    def search_for_player_by_name(self, players, query):
        m, answer = self.search(players, attribute_name="name", query=query)
        if m == 0:
            return False
        return answer

    def search_for_team_from_standing_by_name(self, teams, query):
        m, answer = self.search(teams, attribute_name="team_name", query=query)
        if m == 0:
            return False
        return answer

    @staticmethod
    def search_by_code(dataset, attribute_name, query):
        search = query.lower()
        for index, data in enumerate(dataset):
            code = getattr(data, attribute_name).lower()
            if code == search:
                return dataset[index]
        return False

    @staticmethod
    def search(dataset, attribute_name, query):
        values = [0 for _ in range(0, len(dataset))]
        search = query.lower().split()
        upper_threshold = len(search)
        for index, data in enumerate(dataset):
            data_name = getattr(data, attribute_name).lower()
            search_array = data_name.split()
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
        return max_value, dataset[max_index]
