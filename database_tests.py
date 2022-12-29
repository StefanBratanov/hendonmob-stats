import unittest

from database import *


class Tests(unittest.TestCase):

    def test_saving_and_retrieving_data_for_an_year(self):
        save_year_to_db(1981)
        tournaments_df = get_tournaments(1981)
        results_df = get_results(1981)

        self.assertEqual(tournaments_df.shape[0], 25)
        self.assertListEqual(
            list(tournaments_df.columns.values), tournament_db_columns)

        self.assertEqual(results_df.shape[0], 137)
        self.assertListEqual(
            list(results_df.columns.values), result_db_columns)

        self.assertEqual(tournaments_df['prize_pool'].sum(), 2622860)

        player_df = results_df.loc[results_df['player_id'] == 14]

        self.assertEqual(player_df['place'].tolist(), [12, 2, 7])
        self.assertEqual(player_df['prize'].sum(), 53000)


if __name__ == "__main__":
    unittest.main()
