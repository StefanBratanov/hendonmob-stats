from pathlib import Path
import shutil
import datetime
import os
import pandas as pd
from extractors import *
import urllib3

base_db_dir = os.path.join(Path.home(), "hendonmob-stats")

tournament_db_columns = ['festival_id', 'festival_name', 'festival_url',
                         'id', 'name', 'url', 'venue', 'entries', 'prize_pool']
tournament_db_types = {'festival_id': 'Int64', 'festival_name': 'string', 'festival_url': 'string',
                       'id': 'Int64', 'name': 'string', 'url': 'string', 'venue': 'string', 'entries': 'Int64', 'prize_pool': 'Int64'}
tournament_db_file = "tournaments.parquet.gz"

result_db_columns = ['tournament_id', 'player_id', 'player_name',
                     'player_url', 'player_country', 'place', 'prize']
result_db_types = {'tournament_id': 'Int64', 'player_id': 'Int64', 'player_name': 'string',
                   'player_url': 'string', 'player_country': 'string', 'place': 'Int64', 'prize': 'Int64'}
result_db_file = "results.parquet.gz"


first_year = 1970


def get_year_range() -> List[int]:
    return list(range(first_year, datetime.date.today().year + 1))


def read_parquet_file(file_path: str) -> pd.DataFrame:
    return pd.read_parquet(file_path, engine="fastparquet")


def get_tournament_db_row(festival: Festival, tournament: Tournament) -> dict:
    return {'festival_id': festival.id, 'festival_name': festival.name,
            'festival_url': festival.url, 'id': tournament.id, 'name': tournament.name,
            'url': tournament.url, 'venue': tournament.venue, 'entries': tournament.entries, 'prize_pool': tournament.prize_pool}


def get_result_db_row(tournament: Tournament, result: Result) -> dict:
    return {'tournament_id': tournament.id, 'player_id': result.player.id, 'player_name': result.player.name,
            'player_url': result.player.url, 'player_country': result.player.country, 'place': result.place, 'prize': result.prize}


def get_db_dir(year: int) -> Path:
    return Path(os.path.join(base_db_dir, str(year)))


def save_all_years_to_db():
    for year in get_year_range():
        print("Processing {}".format(year))
        try:
            save_year_to_db(year)
        except:
            print("Failed to process {}".format(year))


def save_year_to_db(year: int):
    # disable requests warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    tournament_df = pd.DataFrame(columns=tournament_db_columns)
    tournament_df = tournament_df.astype(tournament_db_types)
    result_df = pd.DataFrame(columns=result_db_columns)
    result_df = result_df.astype(result_db_types)
    db_dir = get_db_dir(year)
    db_dir.mkdir(parents=True, exist_ok=True)
    festivals = extract_festivals(year)
    print("Extracted {} festival(s) for {}".format(len(festivals), year))
    for f_idx, festival in enumerate(festivals):
        tournament_urls = extract_tournament_urls(festival)
        print("Processing tournament(s) for {} [{}/{}]".format(festival.name,
                                                               f_idx+1, len(festivals)))
        tournament_db_rows = []
        for t_idx, tournament_url in enumerate(tournament_urls):
            tournament = extract_tournament(festival, tournament_url)
            tournament_db_rows.append(
                get_tournament_db_row(festival, tournament))
            result_db_rows = list(map(lambda result: get_result_db_row(
                tournament, result), tournament.results))
            result_df = pd.concat(
                [result_df, pd.DataFrame(result_db_rows).astype(result_db_types)])
            print("Processed {} [{}/{}]".format(tournament.name,
                  t_idx+1, len(tournament_urls)))
        if len(tournament_db_rows) > 0:
            tournament_df = pd.concat(
                [tournament_df, pd.DataFrame(tournament_db_rows).astype(tournament_db_types)])

    tournaments_file = os.path.join(db_dir, tournament_db_file)
    tournament_df.to_parquet(
        tournaments_file, engine="fastparquet", compression="gzip")
    print("Saved {} tournament(s) to {}".format(
        tournament_df.shape[0], tournaments_file))
    results_file = os.path.join(db_dir, result_db_file)
    result_df.to_parquet(
        results_file, engine="fastparquet", compression="gzip")
    print("Saved {} tournament result(s) to {}".format(
        result_df.shape[0], results_file))


def delete_year_from_db(year: int):
    db_dir = get_db_dir(year)
    shutil.rmtree(db_dir)
    print("Removed data from db for {}".format(year))


def get_tournaments(years: List[int] = None) -> pd.DataFrame:
    if years is None:
        years = get_year_range()
    tournaments_df = None
    for year in years:
        db_file_path = os.path.join(get_db_dir(year), tournament_db_file)
        if not os.path.exists(db_file_path):
            continue
        if tournaments_df is None:
            tournaments_df = read_parquet_file(db_file_path)
        else:
            tournaments_df = pd.concat(
                [tournaments_df, read_parquet_file(db_file_path)])
        print("Retrieved tournaments data for {}".format(year))
    return tournaments_df


def get_results(years: List[int] = None) -> pd.DataFrame:
    if years is None:
        years = get_year_range()
    results_df = None
    for year in years:
        db_file_path = os.path.join(get_db_dir(year), result_db_file)
        if not os.path.exists(db_file_path):
            continue
        if results_df is None:
            results_df = read_parquet_file(db_file_path)
        else:
            results_df = pd.concat(
                [results_df, read_parquet_file(db_file_path)])
        print("Retrieved results data for {}".format(year))
    return results_df
