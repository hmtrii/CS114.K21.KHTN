import scrapy
from slugify import slugify
import pandas as pd


class FifaIndexTeamScraper(scrapy.Spider):
    name = "fifa-index-team"
    latest_season = "fifa20"

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
                # "url": url,
            }


def adjust_link(link):
    tail = link.split('/')[-1]
    link = link.replace(tail, 'teams/' + tail)
    return link


links_data = pd.read_csv("project/spiders/link_match.csv")
links = links_data['link-href']
links = links.apply(adjust_link)


class Skysport(scrapy.Spider):
    name = "lineups"

    def start_requests(self):
        urls = links
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_match_page)

    def parse_match_page(self, response):
        date = response.xpath('/html/body/div[6]/div/div[1]/div[2]/p[2]/time/text()').get()
        date = date.split(' ')[-3] + ' ' + date.split(' ')[-2] + ' ' + date.split(' ')[-1]

        home_team, away_team = response.css("span.sdc-site-match-header__team-name-block-target::text").getall()

        home_goals = int(response.css("span.sdc-site-match-header__team-score-block::text").getall()[0])
        away_goals = int(response.css("span.sdc-site-match-header__team-score-block::text").getall()[1])

        home_lineups = []
        away_lineups = []
        for i in range(1, 12):
            path1 = f"/html/body/div[8]/div/div[1]/div/div[1]/div[1]/dl[1]/dt[{i}]/text()"
            path2 = f"/html/body/div[8]/div/div[1]/div/div[1]/div[2]/dl[1]/dt[{i}]/text()"
            home_lineups.append(response.xpath(path1).get())
            away_lineups.append(response.xpath(path2).get())

        yield {
            "date": date,
            "home_team": slugify(home_team),
            "away_team": slugify(away_team),
            "home_goals": int(home_goals),
            "away_goals": int(away_goals),
            "home_lineups": home_lineups,
            "away_lineups": away_lineups,
        }
