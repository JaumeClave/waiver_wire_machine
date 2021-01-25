import time
import random
import argparse
import pandas as pd
pd.options.mode.chained_assignment = None
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import commonallplayers

IS_ACTIVE_KEY = "is_active"
FULL_NAME_KEY = "full_name"
PERSON_ID_KEY = "PERSON_ID"
SEASON_2020 = "2020"
MINUTES_COLUMN = "MIN"
FIELD_GOALS_MADE_COLUMN = "FGM"
FIELD_GOAL_ATTEMPTED_COLUMN = "FGA"
FIELD_GOAL_PERCENTAGE_COLUMN = "FG_PCT"
FREE_THROW_MADE_COLUMN = "FTM"
FREE_THROW_ATTEMPTED_COLUMN = "FTA"
FREE_THROW_PERCENTAGE_COLUMN = "FT_PCT"
THREES_MADE_COLUMN = "FG3M"
POINTS_COLUMN = "PTS"
REBOUNDS_COLUMN = "REB"
ASSITS_COLUMN = "AST"
STEALS_COLUMN = "STL"
BLOCKS_COLUMN = "BLK"
TURNOVERS_COLUMN = "TOV"
MEAN_ROW = "Mean"
PLAYER_COLUMN = "PLAYER"
GAMES_PLAYED = "GAMES"
DISPLAY_FIRST_LAST = "DISPLAY_FIRST_LAST"
COMMON_ALL_PLAYERS ="CommonAllPlayers"


THREE_DECIMAL_FORMAT = "{:,.3f}".format
TWO_DECIMAL_FORMAT = "{:,.2f}".format

CALCULATING_COLUMNS = [FIELD_GOALS_MADE_COLUMN, FIELD_GOAL_ATTEMPTED_COLUMN,
                    FIELD_GOAL_PERCENTAGE_COLUMN, FREE_THROW_MADE_COLUMN,
                    FREE_THROW_ATTEMPTED_COLUMN, FREE_THROW_PERCENTAGE_COLUMN,
                    THREES_MADE_COLUMN, POINTS_COLUMN, REBOUNDS_COLUMN, ASSITS_COLUMN,
                    STEALS_COLUMN, BLOCKS_COLUMN, TURNOVERS_COLUMN]
NINE_CAT_COLUMNS = [FIELD_GOAL_PERCENTAGE_COLUMN, FREE_THROW_PERCENTAGE_COLUMN,
                    THREES_MADE_COLUMN, POINTS_COLUMN, REBOUNDS_COLUMN, ASSITS_COLUMN,
                    STEALS_COLUMN, BLOCKS_COLUMN, TURNOVERS_COLUMN]
THREE_DECIMAL_COLUMNS = [FIELD_GOAL_PERCENTAGE_COLUMN, FREE_THROW_PERCENTAGE_COLUMN]
ONE_DECIMAL_COLUMNS = [THREES_MADE_COLUMN, POINTS_COLUMN, REBOUNDS_COLUMN, ASSITS_COLUMN,
                       STEALS_COLUMN, BLOCKS_COLUMN, TURNOVERS_COLUMN]



def nba_active_players():

    common_all_players = commonallplayers.CommonAllPlayers(is_only_current_season=1)
    common_all_players_dict = common_all_players.get_normalized_dict()[COMMON_ALL_PLAYERS]

    return common_all_players_dict


def move_column_inplace(dataframe, column, position):

    column = dataframe.pop(column)
    dataframe.insert(position, column.name, column)


def true_percentage(dataframe, pct_category):
    no_mean_row_dataframe = dataframe.drop(MEAN_ROW)
    if pct_category == FIELD_GOAL_PERCENTAGE_COLUMN:
        true_field_goal_pct = no_mean_row_dataframe[FIELD_GOALS_MADE_COLUMN].mean() / \
                              no_mean_row_dataframe[FIELD_GOAL_ATTEMPTED_COLUMN].mean()
        dataframe.at[MEAN_ROW, FIELD_GOAL_PERCENTAGE_COLUMN] = true_field_goal_pct

    else:
        true_free_throw_pct = no_mean_row_dataframe[FREE_THROW_MADE_COLUMN].mean() / \
            no_mean_row_dataframe[FREE_THROW_ATTEMPTED_COLUMN].mean()
        dataframe.at[MEAN_ROW, FREE_THROW_PERCENTAGE_COLUMN] = true_free_throw_pct

    return dataframe


def format_dataframe_decimals(dataframe):
    dataframe[THREE_DECIMAL_COLUMNS] = dataframe[THREE_DECIMAL_COLUMNS].applymap \
        (THREE_DECIMAL_FORMAT)
    dataframe[ONE_DECIMAL_COLUMNS] = dataframe[ONE_DECIMAL_COLUMNS].applymap(TWO_DECIMAL_FORMAT)

    return dataframe

def player_average_9cat_stats(player_name, player_data_dict):

    # Get player identifier
    player_name_dict = [player for player in player_data_dict if player[DISPLAY_FIRST_LAST] ==
                        player_name]
    player_id = player_name_dict[0][PERSON_ID_KEY]

    # Player game log
    player_game_log = playergamelog.PlayerGameLog(player_id=player_id, season=SEASON_2020)
    nba_cooldown = random.gammavariate(alpha=9, beta=0.4)
    time.sleep(nba_cooldown)
    player_game_log_dataframe = player_game_log.get_data_frames()[0]

    # Filter for games played
    player_game_log_dataframe = \
    player_game_log_dataframe[player_game_log_dataframe[MINUTES_COLUMN] >= 1]

    # Find true percentages
    player_game_log_dataframe = player_game_log_dataframe[CALCULATING_COLUMNS]
    player_game_log_dataframe.loc[MEAN_ROW] = player_game_log_dataframe.mean()
    player_game_log_dataframe = true_percentage(player_game_log_dataframe,
                                                FIELD_GOAL_PERCENTAGE_COLUMN)
    player_game_log_dataframe = true_percentage(player_game_log_dataframe,
                                                FREE_THROW_PERCENTAGE_COLUMN)

    # Filter for 9cat columns
    player_9cat = player_game_log_dataframe[NINE_CAT_COLUMNS]

    # Formatting columns
    player_9cat = format_dataframe_decimals(player_9cat)

    # Show only averages
    player_9cat_season_average = pd.DataFrame(player_9cat.loc[MEAN_ROW]).T

    # Add player name/games player
    player_9cat_season_average[PLAYER_COLUMN] = player_name
    player_9cat_season_average[GAMES_PLAYED] = len(player_game_log_dataframe)

    # Move PLAYER NAME column
    move_column_inplace(player_9cat_season_average, PLAYER_COLUMN, 0)

    return player_9cat_season_average



def get_player_9cat_season_average(player_name):

    active_player_dict = nba_active_players()
    player_9cat_season_average = player_average_9cat_stats(player_name, active_player_dict)

    return player_9cat_season_average


# To run from the terminal provide the Player Name for which the scraper should return season
# average stats for using the for ```--players``` argument.
# Example: python player_9cat_average.py --players "Obi Toppin"
if __name__ == "__main__":
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
        "--players",
        nargs="*",
        type=str,
        default="",
    )

    # Parse the command line
    ARGS = CLI.parse_args()
    for player in ARGS.players:
        print(get_player_9cat_season_average(player))
