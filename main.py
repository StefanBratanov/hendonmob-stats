from extractors import *

year = 1980

print("Retrieving festivals for {}".format(year))

festivals = extract_festivals(year)

for f_index, festival in enumerate(festivals):
    print(
        "Processing festival [{}/{}]: {}".format(f_index+1, len(festivals), festival.name))
    print("Retrieving tournaments for {}".format(festival.name))
    tournament_urls = extract_tournament_urls(festival)
    for t_index, tournament_url in enumerate(tournament_urls):
        print(
            "Processing tournament [{}/{}]".format(t_index+1, len(tournament_urls)))
        tournament = extract_tournament(festival, tournament_url)
        print(tournament.name)
        print("Venue: {}".format(tournament.venue))
        print("{} entries".format(tournament.entries))
        print("Prize pool is {}".format(tournament.prize_pool))
        if len(tournament.results) > 0:
            print("Winner is {}".format(tournament.results[0].player.name))
