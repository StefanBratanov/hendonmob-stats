import requests
from bs4 import BeautifulSoup
import re
from typing import List, Tuple
from model import *

requests.packages.urllib3.disable_warnings()

hendon_mob_url = "https://pokerdb.thehendonmob.com"


def get_soup(url) -> BeautifulSoup:
    page = requests.get(url, verify=False)
    return BeautifulSoup(page.content, "html.parser")


def text2number(text):
    return int(re.sub(r'[^\d]', "", text))


def get_tournament_info(tournament: Tournament) -> Tuple[TournamentMeta, List[Participant]]:
    soup = get_soup(tournament.url)

    name = soup.select_one("div.content-content h1").text.strip()

    venue = soup.select_one("div.header-image__venue").text.strip()

    key_stats = soup.select("div.key_stats div div")

    entries = None
    prize_pool = None

    for key_stat in key_stats:
        if "Entries" in key_stat.text:
            entries = text2number(key_stat.select_one("div span").text)
        if "Total Prize Pool" in key_stat.text:
            prize_pool = text2number(key_stat.select_one("div span").text)

    tournament_meta = TournamentMeta(name, venue, entries, prize_pool)

    results = soup.select("table.table--event-results tr")

    participants = []
    # skip header
    for result in results[1:]:
        name = result.select_one("td.name a, td.name").text.strip()
        country = result.select_one("td.flag").text.strip()
        place = int(
            re.search(r'\d+', result.select_one("td.place").text).group())
        prize = next((text2number(prize.text) for prize in result.select(
            "td.prize") if prize.text.strip()), None)
        participant = Participant(name, country, place, prize)
        participants.append(participant)

    return tournament_meta, participants


def get_festivals(year) -> List[Festival]:

    url = "{}/festival.php?a=l&m=all&y={}".format(hendon_mob_url, year)

    soup = get_soup(url)

    festivals = []

    festival_tags = filter(lambda tag: str(tag['href'] or '').startswith(
        "/festival"), soup.select("td.db-list__name a"))

    for festival_tag in festival_tags:
        url = "{}{}".format(hendon_mob_url, festival_tag['href'])
        name = festival_tag.text.strip()
        festival = Festival(name, url)
        festivals.append(festival)

    return festivals


def get_tournaments(festival: Festival) -> List[Tournament]:
    soup = get_soup(festival.url)

    tournament_tags = filter(lambda tag: str(tag['href'] or '').startswith(
        "event.php"), soup.select("table.table--festival-schedule td.name a"))

    tournaments = []

    for tournament_tag in tournament_tags:
        url = "{}/{}".format(hendon_mob_url, tournament_tag['href'])
        name = tournament_tag.text.strip()
        tournament = Tournament(name, url)
        tournaments.append(tournament)

    return tournaments


year = 1980

print("Retrieving festivals for {}".format(year))

festivals = get_festivals(year)

for f_index, festival in enumerate(festivals):
    print(
        "Processing festival [{}/{}]: {}".format(f_index+1, len(festivals), festival.name))
    print("Retrieving tournaments for {}".format(festival.name))
    tournaments = get_tournaments(festival)
    for t_index, tournament in enumerate(tournaments):
        print(
            "Processing tournament [{}/{}]: {}".format(t_index+1, len(tournaments), tournament.name))
        tournament_info = get_tournament_info(tournament)
        tournament_meta = tournament_info[0]
        participants = tournament_info[1]
