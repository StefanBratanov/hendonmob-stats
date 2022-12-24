from typing import List


class Festival:
    def __init__(self, id: int, name: str, url: str):
        self.id = id
        self.name = name
        self.url = url


class Player:
    def __init__(self, id: int, name: str, url: str, country: str):
        self.id = id
        self.name = name
        self.url = url
        self.country = country


class Result:
    def __init__(self, player: Player, place: int, prize: int):
        self.player = player
        self.place = place
        self.prize = prize


class Tournament:
    def __init__(self, id: int, name: str, festival: Festival, url: str, venue: str, entries: int, prize_pool: int,
                 results: List[Result]):
        self.id = id
        self.name = name
        self.festival = festival
        self.url = url
        self.venue = venue
        self.entries = entries
        self.prize_pool = prize_pool
        self.results = results
