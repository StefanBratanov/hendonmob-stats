import unittest
import tempfile

import database

from database import save_year_to_db, get_tournaments, get_results, delete_year_from_db


class Tests(unittest.TestCase):

    def setUp(self):
        database.base_db_dir = tempfile.mkdtemp()

    def test_saving_and_retrieving_data_for_an_year(self):
        save_year_to_db(1981)
        tournaments_df = get_tournaments(years=[1981])
        results_df = get_results(years=[1981])

        self.assertEqual(tournaments_df.shape[0], 25)
        self.assertListEqual(
            list(tournaments_df.columns.values), database.tournament_db_columns)

        self.assertEqual(results_df.shape[0], 137)
        self.assertListEqual(
            list(results_df.columns.values), database.result_db_columns)

        self.assertEqual(tournaments_df['prize_pool'].sum(), 2622860)

        player_df = results_df.loc[results_df['player_id'] == 14]

        self.assertEqual(player_df['place'].tolist(), [12, 2, 7])
        self.assertEqual(player_df['prize'].sum(), 53000)

        delete_year_from_db(1981)

        # test deletion
        self.assertIsNone(get_tournaments())
        self.assertIsNone(get_results())

    def test_saving_and_retrieving_data_for_all_years(self):
        # years with not many festivals
        save_year_to_db(1971)
        save_year_to_db(1972)
        save_year_to_db(1973)

        tournaments_df = get_tournaments()
        results_df = get_results()

        self.assertEqual(tournaments_df.shape[0], 14)
        self.assertEqual(results_df.shape[0], 18)

        delete_year_from_db(1971)
        delete_year_from_db(1972)
        delete_year_from_db(1973)


if __name__ == "__main__":
    unittest.main()
