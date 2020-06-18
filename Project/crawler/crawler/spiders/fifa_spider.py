import scrapy
from slugify import slugify

class MatchSpider(scrapy.Spider):
    name = "matchlineups"

    # TODO - want the other names - not full names

    def start_requests(self):
        urls_matches = [
            # EPL
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2019-2020/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2018-2019/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2017-2018/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2016-2017/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2015-2016/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2014-2015/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2013-2014/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2012-2013/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2011-2012/",
            "https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2010-2011/",
            # # Laliga
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2019-2020/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2018-2019/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2017-2018/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2016-2017/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2015-2016/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2014-2015/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2013-2014/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2012-2013/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2011-2012/",
            "https://www.betstudy.com/soccer-stats/c/spain/primera-division/d/results/2010-2011/",
            # # Bundesliga
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2019-2020/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2018-2019/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2017-2018/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2016-2017/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2015-2016/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2014-2015/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2013-2014/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2012-2013/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2011-2012/",
            "https://www.betstudy.com/soccer-stats/c/germany/bundesliga/d/results/2010-2011/",
            # # Serie A
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2019-2020/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2018-2019/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2017-2018/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2016-2017/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2015-2016/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2014-2015/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2013-2014/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2012-2013/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2011-2012/",
            "https://www.betstudy.com/soccer-stats/c/italy/serie-a/d/results/2010-2011/",
            # # Ligue 1
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2019-2020/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2018-2019/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2017-2018/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2016-2017/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2015-2016/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2014-2015/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2013-2014/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2012-2013/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2011-2012/",
            "https://www.betstudy.com/soccer-stats/c/france/ligue-1/d/results/2010-2011/",
        ]
        urls = urls_matches
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_fixtures_page)

    def parse_fixtures_page(self, response):
        for info_button in response.css("ul.action-list").css("a::attr(href)"):
            url = info_button.get()
            yield response.follow(url, self.parse_match_page)

    def parse_match_page(self, response):

        home_team, away_team = response.css("div.player h2 a::text").getall()

        date = response.css("em.date").css("span.timestamp::text").get()

        # url = response.request.url

        # match_number = response.request.url.split("-")[-1].split("/")[0]

        home_goals, away_goals = (
            response.css("div.info strong.score::text").get().split("-")
        )

        for table in response.css("div.table-holder"):
            if table.css("h2::text").get() == "Lineups and subsitutes":
                lineups = table

        home_lineup_css = lineups.css("table.info-table")[0]
        away_lineup_css = lineups.css("table.info-table")[1]

        home_lineup = [
            slugify(x)
            for x in home_lineup_css.css("tr td.left-align")
                .css("a::attr(title)")
                .extract()
        ]
        away_lineup = [
            slugify(x)
            for x in away_lineup_css.css("tr td.left-align")
                .css("a::attr(title)")
                .extract()
        ]

        home_lineup_number = [
            int(x) for x in home_lineup_css.css("tr td.size23 strong::text").getall()
        ]
        away_lineup_number = [
            int(x) for x in away_lineup_css.css("tr td.size23 strong::text").getall()
        ]

        yield {
            "date": date,
            "home team": slugify(home_team),
            "away team": slugify(away_team),
            "home goals": int(home_goals),
            "away goals": int(away_goals),
            "home lineup names": home_lineup,
            "away lineup names": away_lineup,
            "home lineup numbers": home_lineup_number,
            "away lineup numbers": away_lineup_number,
        }



class FifaIndexTeamScraper(scrapy.Spider):
    name = "fifa-index-team"
    latest_season = "fifa19"

    # TODO - run this for extended period of time to get all players

    def start_requests(self):
        urls = [
            # EPL
            "https://www.fifaindex.com/teams/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa19/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa18/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa17/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa16/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa15/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa14/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa13/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa12/?league=13&order=desc",
            "https://www.fifaindex.com/teams/fifa11/?league=13&order=desc",
            # Laliga
            "https://www.fifaindex.com/teams/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa19/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa18/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa17/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa16/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa15/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa14/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa13/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa12/?league=53&order=desc",
            "https://www.fifaindex.com/teams/fifa11/?league=53&order=desc",
            # Bundesliga
            "https://www.fifaindex.com/teams/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa19/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa18/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa17/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa16/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa15/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa14/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa13/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa12/?league=19&order=desc",
            "https://www.fifaindex.com/teams/fifa11/?league=19&order=desc",
            # Seria
            "https://www.fifaindex.com/teams/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa19/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa18/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa17/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa16/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa15/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa14/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa13/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa12/?league=31&order=desc",
            "https://www.fifaindex.com/teams/fifa11/?league=31&order=desc",
            # Ligue 1
            "https://www.fifaindex.com/teams/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa19/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa18/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa17/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa16/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa15/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa14/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa13/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa12/?league=16&order=desc",
            "https://www.fifaindex.com/teams/fifa11/?league=16&order=desc",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for team_row in response.css("table.table-teams tr"):
            link = team_row.css("td a.link-team::attr(href)").get()
            if link:
                if "/team/" in link:
                    yield response.follow(link, callback=self.parse_team)

        for page_link in response.css(".pagination a.btn"):
            text = page_link.css("::text").get()
            next = page_link.attrib["href"]
            if "Next" in text and int(next.split("/")[-2]) < 10:  # < 10 for 1. Bundesliga, < 15 for 2. Bundesliga
                print("Next page:", next)
                yield response.follow(next, callback=self.parse)

    def parse_team(self, response):
        team = slugify(response.css("div h1::text").get())
        print(team)

        players_table = response.css('table.table-players')[0]
        for player in players_table.css('tbody tr'):
            player_name_link = player.css("td:nth-child(6) a.link-player")

            name = player_name_link.attrib["title"]

            url = player_name_link.attrib["href"]

            season = url.split("/")[-2]
            if "/fifa" not in url:
                season = self.latest_season

            number = int(player.css("td:nth-child(1)::text").get())

            nationality = player.css("td:nth-child(4) a::attr(title)").get()

            age = int(player.css("td:nth-child(8)::text").get())

            for position_option in player.css("span.position::text").getall():
                if position_option not in ["Sub", "Res"]:
                    position = position_option
                    break

            rating = player.css("td:nth-child(5) span.rating::text").get()

            yield {
                "name": slugify(name),
                "team": team,
                "position": position,
                "rating": int(rating),
                "number": number,
                "age": age,
                "nationality": slugify(nationality),
                "season": season,
                "url": url,
            }




