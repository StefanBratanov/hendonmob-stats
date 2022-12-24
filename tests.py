import unittest

from extractors import *


class Tests(unittest.TestCase):

    def test_extracting_festivals_for_an_year(self):
        festivals = extract_festivals(1980)
        self.assertEqual(len(festivals), 3)
        self.assertEqual(festivals[0].name,
                         "Amarillo Slim's Superbowl Of Poker")
        self.assertEqual(festivals[0].id, 4096)
        self.assertEqual(
            festivals[0].url, "https://pokerdb.thehendonmob.com/festival.php?a=r&n=4096")

    def test_extracting_tournament_urls(self):
        festival = Festival(39303, "RunGOOD Poker Series - RGPS Contenders Thunder Valley presented by PokerGO",
                            "https://pokerdb.thehendonmob.com/festival.php?a=r&n=39303")

        tournament_urls = extract_tournament_urls(festival)

        self.assertListEqual(tournament_urls, ["https://pokerdb.thehendonmob.com/event.php?a=r&n=780357",
                                               "https://pokerdb.thehendonmob.com/event.php?a=r&n=780361",
                                               "https://pokerdb.thehendonmob.com/event.php?a=r&n=780369",
                                               "https://pokerdb.thehendonmob.com/event.php?a=r&n=780377",
                                               "https://pokerdb.thehendonmob.com/event.php?a=r&n=780385",
                                               "https://pokerdb.thehendonmob.com/event.php?a=r&n=780387"])

    def test_extracting_tournament(self):
        festival = Festival(39177, "Grosvenor UK Poker Tour - GUKPT London Grand Final",
                            "https://pokerdb.thehendonmob.com/festival.php?a=r&n=39177")
        url = "https://pokerdb.thehendonmob.com/event.php?a=r&n=878371"
        tournament = extract_tournament(
            festival, url)

        self.assertEqual(tournament.id, 878371)
        self.assertEqual(
            tournament.name, "£ 1,100 + 150 No Limit Hold'em - GUKPT Main Event")
        self.assertEqual(tournament.festival, festival)
        self.assertEqual(tournament.url, url)
        self.assertEqual(tournament.venue,
                         "The Poker Room formerly The Vic, London")
        self.assertEqual(tournament.entries, 347)
        self.assertEqual(tournament.prize_pool, 457877)

        self.assertEqual(len(tournament.results), 34)

        result = tournament.results[0]

        self.assertEqual(result.place, 1)
        self.assertEqual(result.prize, 112724)
        self.assertEqual(result.player.name, "Jamie Nixon")
        self.assertEqual(result.player.id, 125241)
        self.assertEqual(result.player.country, "England")
        self.assertEqual(
            result.player.url, "https://pokerdb.thehendonmob.com/player.php?a=r&n=125241")


if __name__ == "__main__":
    unittest.main()
