class Festival:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f"{self.name}|{self.url}"


class Tournament:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f"{self.name}|{self.url}"


class TournamentMeta:
    def __init__(self, name, venue, entries, prize_pool):
        self.name = name
        self.venue = venue
        self.entries = entries
        self.prize_pool = prize_pool

    def __repr__(self):
        return f"{self.name}|{self.venue}|{self.entries}|{self.prize_pool}"


class Participant:
    def __init__(self, name, country, place, prize):
        self.name = name
        self.country = country
        self.place = place
        self.prize = prize

    def __repr__(self):
        return f"{self.name}|{self.country}|{self.place}|{self.prize}"
