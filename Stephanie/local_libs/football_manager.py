# from Stephanie.Modules.base_module import BaseModule
from soccerpy.soccer import Soccer
from pyball.ball import Ball
from Stephanie.local_libs.search_module import SearchModule


# noinspection PyUnresolvedReferences
class FootballManager:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.s = SearchModule()
        self.soccer = Soccer(API_KEY=self.API_KEY)
        self.comps = []
        self.comp = None
        self.league_table = None
        self.teams = []
        self.team = None
        self.fixtures = []
        self.team_fixtures = []
        self.standings = []
        self.players = []
        self.news = Ball()

    def get_all_competitions(self):
        self.comps = self.soccer.competition.get_all().competitions
        response = "All competitions I could find are as follows "
        for comp in self.comps:
            comp_names = comp.caption.split()[:-1]
            for comp_name in comp_names:
                if "1" in comp_name:
                    comp_name = "first"
                if "2" in comp_name:
                    comp_name = "second"
                response += "%s " % comp_name
            response += ", "
        return response

    def get_specific_competition(self, competition_id):
        self.comp = self.soccer.competition.get_specific(competition_id).competition
        response = "%s competition is found." % self.comp.caption
        return response

    def get_league_table(self):
        if self.comp:
            self.league_table = self.comp.league_table()
        response = "As of %s matchday, the league standings of %s are as follows " % (self.league_table.matchday,
                                                                                      self.league_table.league_caption)
        self.standings = self.league_table.standing
        for standing in self.standings.teams:
            response += "%s - %s with the total points of %s in %s games, " % (standing.position, standing.team_name,
                                                                               standing.points, standing.played_games)
        return response

    def get_fixtures(self, prev=False):
        if self.comp:
            pass
        matchday = self.comp.current_matchday + 1
        if self.comp.current_matchday == self.comp.number_of_matchdays:
            matchday = self.number_of_matchdays
        if prev:
            matchday = self.comp.current_matchday - 1
        self.fixtures = self.soccer.competition. \
            get_fixtures_by_matchday(self.comp.id, matchday=matchday).fixtures
        response = "The fixtures of %s for %s matchday are as follows " % (self.comp.caption,
                                                                           matchday)
        for index, fixture in enumerate(self.fixtures):
            date = fixture.date[:-1].replace("T", " with timings of ")
            if prev:
                response += " %s hosted %s on %s which resulted in %s %s - %s %s " % (fixture.home_team_name,
                                                                                      fixture.away_team_name,
                                                                                      date,
                                                                                      fixture.home_team_name,
                                                                                      fixture.result.goals_home_team,
                                                                                      fixture.away_team_name,
                                                                                      fixture.result.goals_away_team)
            else:
                response += "%s - %s will host %s on %s, " % (index, fixture.home_team_name,
                                                              fixture.away_team_name, date)
        return response

    def get_team(self, team_id):
        self.team = self.soccer.team.get(team_id).team
        response = "The %s with the code %s is selected." % (self.team.name, self.team.code)
        return response

    def get_team_fixtures(self, prev=False):
        timeframe = "n30"
        if prev:
            timeframe = "p30"
        if self.team:
            pass
        self.team_fixtures = self.soccer.team.get_fixtures_by_time_frame(self.team.id, timeframe).fixtures
        count = len(self.team_fixtures)
        response = "The fixtures for %s for the next %s days in total %s are as follows " % (self.team.name,
                                                                                             timeframe[1:],
                                                                                             count)
        if prev:
            response = "in last %s days among %s fixtures of %s, results were as follows " % (count,
                                                                                              self.team.name,
                                                                                              timeframe[1:])
        for index, fixture in enumerate(self.team_fixtures):
            date = fixture.date[:-1].replace("T", " with timings of ")
            if prev:
                response = " %s hosted %s on %s which resulted in %s %s - %s %s " % (fixture.home_team_name,
                                                                                     fixture.away_team_name,
                                                                                     date,
                                                                                     fixture.home_team_name,
                                                                                     fixture.result.goals_home_team,
                                                                                     fixture.away_team_name,
                                                                                     fixture.result.goals_away_team)
            else:
                response += "%s - %s will host %s on %s, " % (index, fixture.home_team_name,
                                                              fixture.away_team_name, date)

        return response

    def get_players(self):
        if self.team:
            pass
        self.players = self.team.players().players
        response = "All the players present in %s are as follows " % self.team.name
        for player in self.players:
            response += "%s playing as %s of nationality %s, " % (player.name, player.position,
                                                                  player.nationality)
        return response

    def get_news(self, limit=5):
        news = self.news.all.get_news().news_list
        if not news:
            return False
        response = "The latest news all around football word are as follows : "
        for data in news[:limit]:
            response += "%s such as %s, " % (data.title, data.text)
        return response

    def get_competition_news(self, name, limit=5):
        news = self.news.competition.get_news(name).news_list
        if not news:
            return False
        response = "The latest news for %s are as follows : " % name
        for data in news[:limit]:
            response += "%s such as %s, " % (data.title, data.text)
        return response

    def get_team_news(self, team_name, limit=5):
        news = self.news.team.get_news().news_list
        if not news:
            return False
        response = "The latest news for %s are as follows : " % team_name
        for data in news[:limit]:
            response += "%s such as %s, " % (data.title, data.text)
        return response

    def get_team_transfer_talk(self, team_name, limit=5):
        news = self.news.team.transfer_talk().news_list
        if not news:
            return False
        response = "The latest transfer talks for %s are as follows : " % team_name
        for data in news[:limit]:
            response += "%s such as %s, " % (data.title, data.text)
        return response

    def get_team_injury_news(self, team_name, limit=5):
        news = self.news.team.injury_news().news_list
        if not news:
            return False
        response = "The latest injury updates for %s are as follows : " % team_name
        for data in news[:limit]:
            response += "%s such as %s, " % (data.title, data.text)
        return response
