from typing import List
import re

from model import *
from utils import *
from extractors import *

hendon_mob_url = "https://pokerdb.thehendonmob.com"


def extract_tournament(festival: Festival, url: str) -> Tournament:
    soup = get_soup(url)

    id = extract_id(url)

    name = soup.select_one("div.content-content h1").text.strip()

    venue = soup.select_one("div.header-image__venue").text.strip()

    key_stats = soup.select("div.key_stats div div")

    entries = None
    prize_pool = None

    for key_stat in key_stats:
        if "Entries" in key_stat.text:
            entries = text2number(key_stat.select_one("div span").text)
        if "Total Prize Pool" in key_stat.text or "Guaranteed Prize Pool" in key_stat.text:
            prize_pool = text2number(key_stat.select_one("div span").text)
        # use the USD number if present
        if "Total Prize Pool (USD)" in key_stat.text:
            prize_pool = text2number(key_stat.select_one("div span").text)

    results_tag = soup.select("table.table--event-results tr")

    results = []
    # skip header
    for result_tag in results_tag[1:]:
        player_tag = result_tag.select_one("td.name a, td.name")
        player_name = player_tag.text.strip()
        player_id = None
        player_url = None
        maybe_link = player_tag.select_one("a")
        if maybe_link is not None:
            player_url = "{}{}".format(hendon_mob_url, maybe_link['href'])
            player_id = extract_id(player_url)
        player_country = result_tag.select_one("td.flag").text.strip()
        player = Player(player_id, player_name, player_url, player_country)
        place = text2number(result_tag.select_one("td.place").text)
        prize = next((text2number(prize.text) for prize in reversed(result_tag.select(
            "td.prize")) if prize.text.strip()), None)
        result = Result(player, place, prize)
        results.append(result)

    tournament = Tournament(
        id, name, festival, url, venue, entries, prize_pool, results)

    return tournament


def extract_festivals(year) -> List[Festival]:

    url = "{}/festival.php?a=l&m=all&y={}".format(hendon_mob_url, year)

    soup = get_soup(url)

    festivals = []

    festival_tags = filter(lambda tag: str(tag['href'] or '').startswith(
        "/festival"), soup.select("td.db-list__name a"))

    for festival_tag in festival_tags:
        url = "{}{}".format(hendon_mob_url, festival_tag['href'])
        id = extract_id(url)
        name = festival_tag.text.strip()
        festival = Festival(id, name, url)
        festivals.append(festival)

    return festivals


def extract_tournament_urls(festival: Festival) -> List[str]:
    soup = get_soup(festival.url)

    tournament_tags = filter(lambda tag: str(tag['href'] or '').startswith(
        "event.php"), soup.select("table.table--festival-schedule td.name a"))

    tournament_urls = []

    for tournament_tag in tournament_tags:
        url = "{}/{}".format(hendon_mob_url, tournament_tag['href'])
        tournament_urls.append(url)

    return tournament_urls
