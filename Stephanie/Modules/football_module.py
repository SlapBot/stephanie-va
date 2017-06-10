from Stephanie.Modules.base_module import BaseModule
from Stephanie.local_libs.football_manager import FootballManager


class FootballModule(BaseModule):
    modules = (
        ("FooballModule@GetAllCompetitions", ("all", "competitions")),
        ("FooballModule@GetEnglishLeague", ("english", "league")),
        ("FooballModule@GetEnglishSecondLeague", ("english", "second", "league")),
        ("FooballModule@GetGermanLeague", ("german", "league")),
        ("FooballModule@GetGermanSecondLeague", ("german", "second", "league")),
        ("FooballModule@GetFrenchLeague", ("french", "league")),
        ("FooballModule@GetFrenchSecondLeague", ("french", "second", "league")),
        ("FooballModule@GetSpanishLeague", ("spanish", "league")),
        ("FooballModule@GetSpanishSecondLeague", ("spanish", "second", "league")),
        ("FooballModule@GetGermanCup", ("german", "cup")),
        ("FooballModule@GetChampionsLeague", ("champions", "league")),
        ("FooballModule@GetNetherlandsLeague", ("netherlands", "league")),
        ("FooballModule@GetPortugueseLeague", ("portuguese", "league")),
        ("FooballModule@GetItalianLeague", ("italian", "league")),
        ("FooballModule@TeamHandle", ("team", "information")),
        ("FooballModule@GetNews", ("latest", "news")),
    )

    def __init__(self, *args):
        super(FootballModule, self).__init__(*args)
        self.API_KEY = self.get_configuration("api.football.org.key")
        self.fm = FootballManager(self.API_KEY)
        self.team_id = self.get_configuration("favorite_football_team_id")
        self.team_name = self.get_configuration("favorite_football_team_name")
        self.competition_name = self.get_configuration("favorite_football_competition_name")

    def handle(self):
        self.assistant.say("which competition would you like to know about? or maybe your team information? or perhaps some news?")
        text = self.assistant.listen().decipher()
        module_func = self.assistant.understand(self.modules, text)
        getattr(self, module_func)()

    def get_all_competitions(self):
        return self.fm.get_all_competitions()

    def get_english_league(self):
        self.get_general_league(426)

    def get_english_second_league(self):
        self.get_general_league(427)

    def get_german_league(self):
        self.get_general_league(430)

    def get_german_second_league(self):
        self.get_general_league(431)

    def get_spanish_league(self):
        self.get_general_league(439)

    def get_spanish_second_league(self):
        self.get_general_league(437)

    def get_french_league(self):
        self.get_general_league(434)

    def get_french_second_league(self):
        self.get_general_league(435)

    def get_netherlands_league(self):
        self.get_general_league(433)

    def get_portuguese_league(self):
        self.get_general_league(436)

    def get_italian_league(self):
        self.get_general_league(438)

    def get_champions_league(self):
        self.get_general_league(440)

    def get_general_league(self, competition_id):
        active = False
        modules = (
            ("FootballModule@LeagueSpecificNews", ("get", "news")),
            ("FootballModule@LeagueSpecificTable", ("get", "league", "table")),
            ("FootballModule@LeagueSpecificNext_fixtures", ("get", "next", "fixtures")),
            ("FootballModule@LeagueSpecificPrevious_fixtures", ("get", "previous", "fixtures")),
        )
        while not active:
            response = self.fm.get_specific_competition(competition_id)
            self.assistant.say("%s, would you like to know about it's latest news, league table or "
                               " maybe fixtures?" % response)
            text = self.assistant.listen().decipher()
            module_func = self.assistant.understand(modules, text)
            active = getattr(self, module_func)()
        return active

    def league_specific_table(self):
        response = self.fm.get_league_table()
        self.assistant.say(response)
        self.assistant.say("Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def league_specific_next_fixtures(self):
        response = self.fm.get_fixtures()
        self.assistant.say(response)
        self.assistant.say("Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def league_specific_previous_fixtures(self):
        response = self.fm.get_fixtures(prev=True)
        self.assistant.say(response)
        self.assistant.say("Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def team_handle(self):
        active = False
        modules = (
            ("FooballModule@TeamNews", ("get", "news")),
            ("FooballModule@TeamInjuryNews", ("get", "injury", "news")),
            ("FooballModule@TeamTransferTalk", ("get", "transfer", "talk")),
            ("FooballModule@TeamPlayers", ("get", "players")),
            ("FooballModule@TeamNextFixtures", ("get", "next", "fixtures")),
            ("FooballModule@TeamPreviousFixtures", ("get", "previous", "fixtures")),
        )
        while not active:
            response = self.fm.get_team(self.team_id)
            self.assistant.say("%s, would you like to know about it's latest news, transfer talks or "
                               " maybe fixtures?" % response)
            text = self.assistant.listen().decipher()
            module_func = self.assistant.understand(modules, text)
            active = getattr(self, module_func)()
        return active

    def team_next_fixtures(self):
        response = self.fm.get_team_fixtures()
        self.assistant.say(response)
        self.assistant.say("Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def team_previous_fixtures(self):
        response = self.fm.get_team_fixtures(prev=True)
        self.assistant.say(response)
        self.assistant.say("Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def league_specific_news(self):
        response = self.fm.get_competition_news(self.competition_name)
        self.assistant.say(response)
        self.assistant.say("For more information, check the sportsmole.co.uk, Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def team_specific_news(self):
        response = self.fm.get_competition_news(self.competition_name)
        self.assistant.say(response)
        self.assistant.say("For more information, check the sportsmole.co.uk, Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def team_news(self):
        response = self.fm.get_team_news(self.team_name)
        self.assistant.say(response)
        self.assistant.say("For more information, check the sportsmole.co.uk, Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def team_injury_news(self):
        response = self.fm.get_team_injury_news(self.team_name)
        self.assistant.say(response)
        self.assistant.say("For more information, check the sportsmole.co.uk, Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def team_transfer_talk(self):
        response = self.fm.get_team_news(self.team_name)
        self.assistant.say(response)
        self.assistant.say("For more information, check the sportsmole.co.uk, Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False

    def get_news(self):
        response = self.fm.get_news()
        self.assistant.say(response)
        self.assistant.say("For more information, check the sportsmole.co.uk, Any other information, you would like to know about? If yes then what would "
                           "it be?")
        text = self.assistant.listen().decipher()
        if text.upper() in self.NEGATIVE:
            self.assistant.say("Alright then blimey.")
            return "Alright then blimey."
        return False
