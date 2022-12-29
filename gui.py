from pandasgui import show
from database import *

tournaments_df = get_tournaments()
results_df = get_results()

show(tournaments_df, results_df)
