import json
import requests
import pandas as pd
import streamlit as st
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from src.data import player_9cat_average as p9ca
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import commonplayerinfo
from src.data import all_functions as af


JSON_FOLDER = r"C:\Users\Jaume\Documents\Python Projects\waiver_wire_machine\references\oauth2.json"
NBA = "nba"
SEASON = 2020
GAMES_COLUMN = "GAMES"
MEAN_ROW = "mean"
TEAM_KEY = "team_key"
PLAYER_COLUMN = "PLAYER"
TEAM_COLUMN = "TEAM"
EDITORIAL_TEAM_FULL_NAME = "editorial_team_full_name"
UNIFORM_NUMBER = "uniform_number"
COMMON_ALL_PLAYERS = "CommonAllPlayers"
PERSON_ID_KEY = "PERSON_ID"
TEAM_CITY_KEY = "TEAM_CITY"
TEAM_NAME_KEY = "TEAM_NAME"
COMMON_PLAYER_INFO = "CommonPlayerInfo"
JERSEY_KEY = "JERSEY"
DISPLAY_FIRST_LAST = "DISPLAY_FIRST_LAST"
RANK_SUFFIX = "_RANK"
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
CATS_COLUMNS = "CATS"
POWER_RANK_COLUMN = "Power_Rank"
PR_COLUMN = "PR"
PLAYER_ID_KEY = "player_id"
NAME_KEY = "name"
LSCD_KEY = "lscd"
MSCD_KEY = "mscd"
G_KEY = "g"
GID_KEY = "gid"
GAME_ID_KEY = "game_id"
GDATE_KEY = "gdte"
GAME_DATE_KEY = "game_date"
V_KEY = "v"
TID_KEY = "tid"
VISITORS_TEAM_ID_KEY = "visitors_tid"
VISITORS_KEY = "visitors"
TC_KEY = "tc"
TN_KEY = "tn"
H_KEY = "h"
HOME_TEAM_ID_KEY = "home_tid"
HOME_KEY = "home"
TOTAL_ROW = "total"
INDEX_COLUMN = "index"
NBA_NAME_LA_CLIPPERS = "LA Clippers"
YAHOO_NAME_LA_CLIPPERS = "Los Angeles Clippers"
FANTASY_CONTENT_KEY = "fantasy_content"
LEAGUE_KEY = "league"
SCOREBOARD_KEY = "scoreboard"
ZERO_KEY = "0"
MATCHUPS_KEY = "matchups"
MATCHUP_KEY = "matchup"
TEAMS_KEY = "teams"
ONE_KEY = "1"
TEAM_KEY_2 = "team"
NAME_KEY = "name"
TEAM_STATS_KEY = "team_stats"
STATS_KEY = "stats"
STAT_KEY = "stat"
VALUE_KEY = "value"
RANK_KEY = "rank"
CURRENT_COLUMN = "Current"
NEW_COLUMN = "New"
DIFFERENCE_COLUMN = "Difference"
MATCHUP_COLUMNS = [af.PLAYER_COLUMN] + af.NINE_CAT_COLUMNS
THREE_DECIMAL_COLUMNS = [FIELD_GOAL_PERCENTAGE_COLUMN, FREE_THROW_PERCENTAGE_COLUMN]
ONE_DECIMAL_COLUMNS = [THREES_MADE_COLUMN, POINTS_COLUMN, REBOUNDS_COLUMN, ASSITS_COLUMN,
                       STEALS_COLUMN, BLOCKS_COLUMN, TURNOVERS_COLUMN]
STREAMLIT_TABLE_FORMAT = {"FG_PCT": p9ca.THREE_DECIMAL_FORMAT, "FT_PCT": p9ca.THREE_DECIMAL_FORMAT,
                          "FG3M": p9ca.TWO_DECIMAL_FORMAT, "PTS": p9ca.TWO_DECIMAL_FORMAT,
                          "REB": p9ca.TWO_DECIMAL_FORMAT, "AST": p9ca.TWO_DECIMAL_FORMAT,
                          "STL": p9ca.TWO_DECIMAL_FORMAT, "BLK": p9ca.TWO_DECIMAL_FORMAT,
                          "TOV": p9ca.TWO_DECIMAL_FORMAT}

ZERO_DECIMAL_FORMAT = "{:d}".format
STREAMLIT_LIVE_SCORES_TABLE_FORMAT = {"FG_PCT": p9ca.THREE_DECIMAL_FORMAT,
                                      "FT_PCT": p9ca.THREE_DECIMAL_FORMAT,
                          "FG3M": ZERO_DECIMAL_FORMAT, "PTS": ZERO_DECIMAL_FORMAT,
                          "REB": ZERO_DECIMAL_FORMAT, "AST": ZERO_DECIMAL_FORMAT,
                          "STL": ZERO_DECIMAL_FORMAT, "BLK": ZERO_DECIMAL_FORMAT,
                          "TOV": ZERO_DECIMAL_FORMAT}
COLUMN_9CAT_DECIMAL_FORMAT = {af.FIELD_GOAL_PERCENTAGE_COLUMN: af.THREE_DECIMAL_FORMAT,
                              af.FREE_THROW_PERCENTAGE_COLUMN: af.THREE_DECIMAL_FORMAT,
                              af.THREES_MADE_COLUMN: af.TWO_DECIMAL_FORMAT,
                              af.POINTS_COLUMN: af.TWO_DECIMAL_FORMAT,
                              af.REBOUNDS_COLUMN: af.TWO_DECIMAL_FORMAT,
                              af.ASSITS_COLUMN: af.TWO_DECIMAL_FORMAT,
                              af.STEALS_COLUMN: af.TWO_DECIMAL_FORMAT,
                              af.BLOCKS_COLUMN: af.TWO_DECIMAL_FORMAT,
                              af.TURNOVERS_COLUMN: af.TWO_DECIMAL_FORMAT}
LALALAND = {'team_key': '402.l.55374.t.1', 'name': 'LaLaLand'}
AUTOPICK = {'team_key': '402.l.55374.t.2', 'name': 'Autopick'}
CRABBEHERBYTHEPUSSY = {'team_key': '402.l.55374.t.3', 'name': 'CrabbeHerByThePussy'}
MAGICS_JOHNSON = {'team_key': '402.l.55374.t.4', 'name': "Magic's Johnson"}
MCCURRY = {'team_key': '402.l.55374.t.5', 'name': 'McCurry'}
NUNN_OF_YALL_BETTA = {'team_key': '402.l.55374.t.6', 'name': "Nunn of Y'all Betta"}
RUSTY_CUNTBROOKS = {'team_key': '402.l.55374.t.7', 'name': 'Russty Cuntbrooks'}
WAKANDA_FOREVER = {'team_key': '402.l.55374.t.8', 'name': 'Wakanda Forever'}
SWAGGY_P = {'team_key': '402.l.55374.t.9', 'name': 'Swaggy P'}
YOBITCH_TOPPIN_ME = {'team_key': '402.l.55374.t.10', 'name': 'yOBItch Toppin Me'}
TVONS_TIP_TOP_TEAM = {'team_key': '402.l.55374.t.11', 'name': "Tvon's Tip-Top Team"}
EL_LADRON_DE_CABRAS = {'team_key': '402.l.55374.t.12', 'name': 'El Ladrón de Cabras'}
league_team_list = [LALALAND, AUTOPICK, CRABBEHERBYTHEPUSSY, MAGICS_JOHNSON, MCCURRY,
                    NUNN_OF_YALL_BETTA, RUSTY_CUNTBROOKS, WAKANDA_FOREVER, SWAGGY_P,
                    YOBITCH_TOPPIN_ME, TVONS_TIP_TOP_TEAM, EL_LADRON_DE_CABRAS]
LEAGUE_TEAM_NAMES = [AUTOPICK[NAME_KEY], CRABBEHERBYTHEPUSSY[NAME_KEY],
                     EL_LADRON_DE_CABRAS[NAME_KEY], LALALAND[NAME_KEY], MAGICS_JOHNSON[NAME_KEY],
                     MCCURRY[NAME_KEY], NUNN_OF_YALL_BETTA[NAME_KEY], RUSTY_CUNTBROOKS[NAME_KEY],
                     SWAGGY_P[NAME_KEY], TVONS_TIP_TOP_TEAM[NAME_KEY], WAKANDA_FOREVER[NAME_KEY],
                     YOBITCH_TOPPIN_ME[NAME_KEY]]

def yahoo_fantasy_api_authentication():
    """
    Function authenticates to Yahoo Fantasy API via keys in a file.
    return sc: Yahoo Oauth token
    """
    sc = OAuth2(None, None, from_file=JSON_FOLDER)
    return sc

def yahoo_fantasy_league(sc):
    """
    Function returns league constructor for logged in user via the Yahoo Oauth token.
    param sc: Yahoo Oauth token
    return league: Yahoo League constructor
    """
    gm = yfa.Game(sc, NBA)
    league_id_list = gm.league_ids(year=SEASON)
    league_id = "".join(str(id) for id in league_id_list)
    league = gm.to_league(league_id)
    return league

def yahoo_player_team_and_jersey(player_name):
    """
    Function finds a players Yahoo NBA team and jersey number from a player name.
    param player_name (string): name of player
    return players_team (string): NBA team player is rostered at
    return players_number (string): NBA player jersey number
    """
    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    player_details_dictionary = league.player_details(player_name)
    players_team = player_details_dictionary[0][EDITORIAL_TEAM_FULL_NAME]
    players_number = player_details_dictionary[0][UNIFORM_NUMBER]
    return players_team, players_number

def player_ids_by_nba_team_name(nba_team):
    """
    Function returns the NBA Stats Ids of all players on a certain NBA team.
    param nab_team (string): NBA team name
    return player_ids_in_team_list (list): ids of rostered players in NBA team
    """
    common_all_players = commonallplayers.CommonAllPlayers(is_only_current_season=1)
    common_all_players_dict = common_all_players.get_normalized_dict()[COMMON_ALL_PLAYERS]
    player_ids_in_team_list = [player[PERSON_ID_KEY] for player in common_all_players_dict if
                               player[TEAM_CITY_KEY] + " " + player[TEAM_NAME_KEY] == nba_team]
    return player_ids_in_team_list

def nba_player_name_from_jersey_search(team_player_ids, yahoo_jersey_number):
    """
    Function searches NBA Stats jersey numbers for all players in a player list. If a match is
    found, that NBA Stats jersey number is used to return the NBA Stats player name owning that
    jersey.
    param team_player_ids (list): ids of players in searched team
    param yahoo_jersey_number (string): players Yahoo jersey number
    return nba_name (string): name of player in NBA Stats
    """
    for id in team_player_ids:
        nba_jersey_number = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict()[
            COMMON_PLAYER_INFO][0][JERSEY_KEY]
        if nba_jersey_number == yahoo_jersey_number:
            nba_name = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict()[
                COMMON_PLAYER_INFO][0][DISPLAY_FIRST_LAST]
            return nba_name

def yahoo_name_to_nba_name(yahoo_player_name):
    """
    Function expectes a Yahoo player name and it will find the players Team Name and Jersey
    Number. It then searches the NBA API for Player IDs belonging to found Team Name. For every
    Player ID it searches their Jersey Number. When there is a match, it returns the NBA Player
    Name.
    param yahoo_player_name (string): name of player in Yahoo
    return nba_player_name (string): name of player in NBA Stats
    """
    player_team, player_number = yahoo_player_team_and_jersey(yahoo_player_name)
    player_ids_in_team_list = player_ids_by_nba_team_name(player_team)
    nba_player_name = nba_player_name_from_jersey_search(player_ids_in_team_list, player_number)
    return nba_player_name

def create_roster_dataframe(player_list):
    """
    Function creates a dataframe filled with rows of player average 9cat season stats. A player
    list is looped and for each player name, a dataframe row is created. If the Yahoo player name
    does not match the NBA player name, a function to convert Yahoo to NBA name is called.
    @param player_list: list of player names
    @return roster_dataframe: dataframe with season average 9cat stats for player list
    """
    active_players = p9ca.nba_active_players()
    roster_dataframe = pd.DataFrame()
    for player in player_list:
        try:
            roster_dataframe = roster_dataframe.append(p9ca.player_average_9cat_stats(player,
                                                                                      active_players))
        except IndexError:
            nba_player_name = yahoo_name_to_nba_name(player)
            roster_dataframe = roster_dataframe.append(p9ca.player_average_9cat_stats(nba_player_name,
                                                                                      active_players))
        except:
            print(f"Can't find player {player}")
    roster_dataframe.reset_index(inplace=True, drop=True)
    return roster_dataframe

def format_roster_dataframe(roster_dataframe):
    """
    Function formats a dataframe by changing all 9cat columns to dtype float.
    @param roster_dataframe: dataframe with season average 9cat stats for player list
    @return: formatted dataframe with season average 9cat stats for player list
    """
    for column in roster_dataframe.columns[1:]:
        roster_dataframe[column] = roster_dataframe[column].astype(float)
    roster_dataframe.loc[MEAN_ROW] = roster_dataframe.mean()
    roster_dataframe = p9ca.format_dataframe_decimals(roster_dataframe)
    try:
        roster_dataframe.drop(GAMES_COLUMN, axis=1, inplace=True)
    except:
        pass
    return roster_dataframe

def team_9cat_average_stats(team_dictionary, league):
    """
    Function pipelines the process involved in creating a season average 9cat stats dataframe for a
    team in the league.
    @param team_dictionary: dictionary containing team information from league
    @param league: Yahoo League constructor
    @return: formatted dataframe with season average 9cat stats
    """
    team = league.to_team(team_dictionary[TEAM_KEY])
    team_roster = team.roster()
    player_in_team_list = [player[NAME_KEY] for player in team_roster]
    roster_dataframe = create_roster_dataframe(player_in_team_list)
    roster_dataframe = format_roster_dataframe(roster_dataframe)
    return roster_dataframe

def fantasy_team_mean_stats(roster_dataframe, team_dictionary):
    """
    Function filters and returns the season average 9cat stats dataframe by the "mean" row.
    @param roster_dataframe: formatted dataframe with season average 9cat stats
    @param team_dictionary: dictionary containing team information from league
    @return: 1x10 dataframe showing average 9cat stats for an entire roster
    """
    mean_series = roster_dataframe.loc[MEAN_ROW]
    mean_series[PLAYER_COLUMN] = team_dictionary[NAME_KEY]
    team_mean_dataframe = pd.DataFrame(mean_series).T
    team_mean_dataframe = team_mean_dataframe.rename(columns={PLAYER_COLUMN: TEAM_COLUMN})
    team_mean_dataframe.reset_index(inplace=True, drop=True)
    return team_mean_dataframe

def player_to_team_mean_stats(team_dictionary, league):
    """
    This function creates a dataframe containing the season averaged stats for each player on a
    Fantasy Team. It then finds the average stats for the entire team and returns a single row
    dataframe with the Fantasy Team name and its seasoned averaged 9cat stats.
    @param team_dictionary: dictionary containing team information from league
    @param league: Yahoo League constructor
    @return: 1x10 dataframe showing average 9cat stats for an entire roster
    """
    roster_dataframe = team_9cat_average_stats(team_dictionary, league)
    team_mean_dataframe = fantasy_team_mean_stats(roster_dataframe, team_dictionary)
    return team_mean_dataframe

@st.cache(show_spinner=False)
def league_averages(league_team_list):
    """
    Function creates a dataframe with a row for each Yahoo Fantasy team in the league. The
    columns of the dataframe are the teams mean 9cat stats (made up of each owned players 9cat
    season stats). Function can take up to 15 minutes to run.
    @param league_team_list: list of dictionaries containing information on each team in the league
    @return: dataframe with each Yahoo Fantasy teams season averaged 9cat stats
    """
    league_averages_dataframe = pd.DataFrame()
    for team in league_team_list:
        sc = yahoo_fantasy_api_authentication()
        league = yahoo_fantasy_league(sc)
        league_averages_dataframe = league_averages_dataframe.append(player_to_team_mean_stats
                                                                     (team, league))
    league_averages_dataframe.reset_index(drop=True, inplace=True)
    return league_averages_dataframe

def yahoo_player_team_and_jersey(player_name):
    """
    Function finds a players real NBA team and jersey number from player name.
    @param player_name: name of player on Yahoo Fantasy
    @return players_team: NBA team player is active on
    @return players_number: jersey number player wears
    """
    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    player_details_dictionary = league.player_details(player_name)
    players_team = player_details_dictionary[0][EDITORIAL_TEAM_FULL_NAME]
    players_number = player_details_dictionary[0][UNIFORM_NUMBER]
    return players_team, players_number

def player_ids_by_nba_team_name(nba_team):
    """
    Function finds all NBA Stats player ids for a provided NBA team name
    @param nba_team: name of NBA team
    @return: list of NBA Stats player ids in NBA team
    """
    common_all_players = commonallplayers.CommonAllPlayers(is_only_current_season=1)
    common_all_players_dict = common_all_players.get_normalized_dict()[COMMON_ALL_PLAYERS]
    player_ids_in_team_list = [player[PERSON_ID_KEY] for player in common_all_players_dict if \
        player[TEAM_CITY_KEY] + " " + player[TEAM_NAME_KEY] == nba_team]
    return player_ids_in_team_list

def nba_player_name_from_jersey_search(team_player_ids, yahoo_jersey_number):
    """
    Function uses a list of NBA Stats player ids and returns NBA Stats jersey numbers for each
    id. If the NBA Stats jersey number matches the provided Yahoo Fantasy jersey number,
    the NBA Stats name of the player that wears that jersey will be returned.
    @param team_player_ids: list of NBA Stats player ids
    @param yahoo_jersey_number: Yahoo Fantasy jersey number player wears
    @return: NBA Stats player name
    """
    for id in team_player_ids:
        nba_jersey_number = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict() \
            [COMMON_PLAYER_INFO][0][JERSEY_KEY]
        if nba_jersey_number == yahoo_jersey_number:
            nba_name = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict() \
            [COMMON_PLAYER_INFO][0][DISPLAY_FIRST_LAST]
            return nba_name

def yahoo_name_to_nba_name(yahoo_player_name):
    """
    Function expects a Yahoo player name and it will find the players Team Name and Jersey
    Number. It then searches the NBA API for Player IDs belonging to found Team Name. For every
    Player ID it searches their Jersey Number. When there is a match, it returns the NBA Player
    Name.
    @param yahoo_player_name: name of player on Yahoo Fantasy
    @return: name of player on NBA Stats
    """
    player_team, player_number = yahoo_player_team_and_jersey(yahoo_player_name)
    player_ids_in_team_list = player_ids_by_nba_team_name(player_team)
    nba_player_name = nba_player_name_from_jersey_search(player_ids_in_team_list, player_number)
    return nba_player_name

# Function to return team dataframe with 9cat averages
def remove_mean_and_player(team_players_9cat_stats_dataframe, player_to_drop):
    """
    Function takes a Yahoo Fantasy teams average 9cat stat roster and removes a row from it,
    corresponding, to the provided player from the player_to_drop parameter.
    @param team_players_9cat_stats_dataframe: formatted dataframe with season average 9cat stats
    for each player rostered on a team
    @param player_to_drop: name of player to be dropped from team
    @return: formatted dataframe with season average 9cat stats less player_to_drop row
    """
    team_players_9cat_stats_dataframe = team_players_9cat_stats_dataframe.drop(MEAN_ROW)
    team_players_9cat_stats_dataframe = \
        team_players_9cat_stats_dataframe[~team_players_9cat_stats_dataframe[
            PLAYER_COLUMN].str.contains(player_to_drop)]
    return team_players_9cat_stats_dataframe

@st.cache(show_spinner=False)
def waiver_add_and_drop(fantasy_team, player_to_drop, player_to_add):
    """
    Function simulates a player add/drop transaction. First a Yahoo Fantasy teams rostered season
    average 9cat stats dataframe is calculated. The entire current rosters average 9cat stats are
    calculated. The row containing the player name from parameter player_to_drop is removed and a
    player and his season average 9cat stats from the player_to_add parameter is added to the
    team dataframe. The entire new rosters average 9cat stats are calculated.
    @param fantasy_team: dictionary containing team information from league
    @param player_to_drop: name of player to drop from team
    @param player_to_add: name of player to add to team (free agent)
    @return team_players_9cat_stats_dataframe: current team rostered season average 9cat stats
    dataframe
    @return current_team_9cat_average_stats: current team rostered season average 9cat stats mean
    row
    @return new_team_9cat_average_stats_dataframe: new team rostered season average 9cat stats
    dataframe
    @return new_team_9cat_average_stats: new team rostered season average 9cat stats mean row
    """
    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    team_players_9cat_stats_dataframe = team_9cat_average_stats(fantasy_team, league)
    current_team_9cat_average_stats = pd.DataFrame(team_players_9cat_stats_dataframe
                                                   .loc[MEAN_ROW]).T.drop(PLAYER_COLUMN, axis=1)
    removed_mean_dropped_player_dataframe = remove_mean_and_player\
        (team_players_9cat_stats_dataframe, player_to_drop)
    added_player_9cat_averages = p9ca.get_player_9cat_season_average(player_to_add)
    new_team_9cat_average_stats_dataframe = removed_mean_dropped_player_dataframe.append\
        (added_player_9cat_averages)
    new_team_9cat_average_stats_dataframe.reset_index(inplace=True, drop=True)
    new_team_9cat_average_stats_dataframe = format_roster_dataframe \
        (new_team_9cat_average_stats_dataframe)
    new_team_9cat_average_stats = pd.DataFrame(new_team_9cat_average_stats_dataframe
                                                   .loc[MEAN_ROW]).T.drop(PLAYER_COLUMN, axis=1)
    return team_players_9cat_stats_dataframe, current_team_9cat_average_stats, \
           new_team_9cat_average_stats_dataframe, new_team_9cat_average_stats

# Format and find 9cat differences
def remove_player_and_float_convert(dataframe):
    """
    Function cleans dataframe by converting all columns to dtype float
    @param dataframe: dataframe with columns to convert
    @return: converted dataframe
    """
    for column in dataframe.columns:
        dataframe[column] = dataframe[column].astype(float)
    return dataframe

def drop_add_mean_9cat_difference(current_9cat, new_9cat):
    """
    Function finds the difference in each 9cat stat by subtracting the current 9cat stats to the
    new 9cat stats (found when a player is dropped and FA is added)
    @param current_9cat: current team rostered season average 9cat stats mean dataframe row
    @param new_9cat: new team rostered season average 9cat stats mean dataframe row
    @return: 1x9 dataframe containing difference in 9cat stats
    """
    current_9cat = remove_player_and_float_convert(current_9cat)
    new_9cat = remove_player_and_float_convert(new_9cat)
    difference_9cat = new_9cat.subtract(current_9cat)
    return difference_9cat

# Visualise current, new and difference
def visualise_team_9cat_averages(player_to_drop, player_to_add, current_9cat, new_9cat,
                                 difference_9cat, visualise=True):
    if visualise:
        print(f"You are dropping {player_to_drop} and adding {player_to_add}! \n")
        print("The current team 9cat averages are:\n")
        print(current_9cat)
        print("\n")
        print("The new team 9cat averages are:\n")
        print(new_9cat)
        print("\n")
        print("The difference 9cat averages are:\n")
        print(difference_9cat)
        print("\n")
    else:
        pass

# Function for the entire process
@st.cache(allow_output_mutation=True, show_spinner=False)
def compare_team_9cats_on_transaction(team, player_to_drop, player_to_add, visualise=True):
    """
    Function pipelines the process involved in simulating a player add/drop transaction and
    calculates 9cat stat differences between current and new roster average 9cat stat dataframes.
    @param team: dictionary containing team information from league
    @param player_to_drop: name of player to drop from team
    @param player_to_add: name of player to add to team (free agent)
    @param visualise: prints current/new/differnece dataframes
    @return current_players_9cat_averages: current team rostered season average 9cat stats dataframe
    @return current_team_9cat_averages: current team rostered season average 9cat stats mean row
    @return new_players_9cat_averages: new team rostered season average 9cat stats dataframe
    @return new_team_9cat_averages: new team rostered season average 9cat stats mean row
    @return difference_team_9cat_averages: 1x9 dataframe containing difference in 9cat stats
    """
    current_players_9cat_averages, current_team_9cat_averages, new_players_9cat_averages, \
    new_team_9cat_averages = waiver_add_and_drop(team, player_to_drop, player_to_add)
    difference_team_9cat_averages = drop_add_mean_9cat_difference(current_team_9cat_averages,
                                                  new_team_9cat_averages)
    visualise_team_9cat_averages(player_to_drop, player_to_add, current_team_9cat_averages,
                             new_team_9cat_averages, difference_team_9cat_averages, visualise)
    return current_players_9cat_averages, current_team_9cat_averages, new_players_9cat_averages, \
           new_team_9cat_averages, difference_team_9cat_averages

def new_league_9cat_averages(league_average_dataframe, team, new_team_9cat_averages):
    """
    Function calculates the new league averages dataframe by first removing the current teams row
    via the team parameter. The new team 9cat average dataframe is appended to the league
    averages dataframe.
    @param league_average_dataframe: dataframe with each Yahoo Fantasy teams season averaged 9cat
    stats
    @param team: dictionary containing team information from league
    @param new_team_9cat_averages: new team rostered season average 9cat stats mean row
    @return: dataframe with each Yahoo Fantasy teams season averaged 9cat stats plus new team stats
    """
    removed_team_dataframe = league_average_dataframe[~league_average_dataframe[
        TEAM_COLUMN].str.contains(team[NAME_KEY])]
    new_team_9cat_averages[TEAM_COLUMN] = team[NAME_KEY]
    added_team_dataframe = removed_team_dataframe.append(new_team_9cat_averages)
    added_team_dataframe.reset_index(drop=True, inplace=True)
    return added_team_dataframe

def team_dataframe_column_float(roster_dataframe):
    """
    Function cleans roster dataframe by converting all columns (except PLAYER) to dtype float
    @param roster_dataframe: roster dataframe with columns to convert
    @return: converted roster dataframe
    """

    for column in roster_dataframe.columns[1:]:
        try:
            roster_dataframe[column] = roster_dataframe[column].astype(float)
        except:
            pass
    return roster_dataframe

def power_ranking_change(league_averages_dataframe, team, new_team_9cat_averages):
    """

    @param league_averages_dataframe:
    @param team:
    @param new_team_9cat_averages:
    @return:
    """
    # New league average dataframe
    new_league_averages_dataframe = new_league_9cat_averages(league_averages_dataframe,
                                                          team, new_team_9cat_averages)
    new_league_averages_dataframe = team_dataframe_column_float(new_league_averages_dataframe)
    new_league_averages_dataframe = new_league_averages_dataframe.sort_values(TEAM_COLUMN)
    # Get new rankings
    new_league_power_rankings = power_rankings(new_league_averages_dataframe).sort_values(TEAM_COLUMN)
    # Get current rankings
    current_league_power_rankings = power_rankings(league_averages_dataframe).sort_values(TEAM_COLUMN)
    # Drop Team column
    new_league_power_rankings_team = new_league_power_rankings.reset_index(drop=True)
    new_league_power_rankings = new_league_power_rankings_team.drop(TEAM_COLUMN, axis=1)
    current_league_power_rankings = current_league_power_rankings.reset_index(drop=True)
    current_league_power_rankings = current_league_power_rankings.drop(TEAM_COLUMN, axis=1)
    # Difference
    power_rankings_difference = new_league_power_rankings.subtract(current_league_power_rankings)
    # Sorted teams list
    teams = list(league_averages_dataframe.sort_values(TEAM_COLUMN)[TEAM_COLUMN])
    # Add teams column
    power_rankings_difference[TEAM_COLUMN] = teams
    # Rearrange columns
    columns = list(power_rankings_difference.columns)
    columns = [columns[-1]] + columns[:-1]
    power_rankings_difference = power_rankings_difference[columns]
    return new_league_averages_dataframe, new_league_power_rankings_team, power_rankings_difference


# Function power ranking
def power_rankings(dataframe):

    power_ranking_dataframe = dataframe.copy()
    try:
        power_ranking_dataframe.drop(MEAN_ROW, inplace=True)
    except KeyError:
        pass
    for column in power_ranking_dataframe.columns[1:]:
        if column != "TOV":
            sorted_points = power_ranking_dataframe[column].sort_values(ascending=False)
        else:
            sorted_points = power_ranking_dataframe[column].sort_values(ascending=True)
        sorted_points.drop_duplicates(inplace=True)

        sorting_dictionary = dict()

        count = 1
        for point in sorted_points:
            sorting_dictionary[point] = count
            count += 1

        power_ranking_dataframe[column + " "] = power_ranking_dataframe[column].map\
            (sorting_dictionary)

    power_ranking_dataframe.drop(dataframe.columns[1:], axis=1, inplace=True)

    return power_ranking_dataframe


def color_negative_red(val):
    """
    Takes a scalar and returns a string with the css property `'color: #EC7063'` for negative
    strings, black when value is zero (0) and green when value is positive. This is used for all
    9cat columns except for TOV.
    """
    if val == 0:
        color = "#000000"
    elif val < 0:
        color = "#EC7063"
    else:
        color = '#52BE80'
    return 'color: %s' % color

def color_negative_red_tov(val):
    """
    Takes a scalar and returns a string with the css property `'color: red'` for positive
    strings, black when value is zero (0) and green when value is negative. This is used for the
    TOV category column.
    """
    if val == 0:
        color = "#000000"
    elif val > 0:
        color = "#EC7063"
    else:
        color = '#52BE80'
    return 'color: %s' % color

def color_power_rank(val):
    """
    Takes a scalar and returns a string with the css property 'color' for different possible
    values. This is used during the power ranking dataframe for all 9cat columns except for TOV.
    """
    if int(val[-3:-1]) == 0:
        color = "#FFFFFF"
    elif int(val[-3:-1]) == 1:
        color = "#db9d9d"
    elif int(val[-3:-1]) == -1:
        color = '#abe5a8'
    elif int(val[-3:-1]) < -1:
        color = "#52BE80"
    else:
        color = "#EC7063"
    return 'background-color: %s' % color

def color_power_rank_tov(val):
    """
    Takes a scalar and returns a string with the css property 'color' for different possible
    values. This is used during the power ranking dataframe for the TOV category column.
    """
    if int(val[-3:-1]) == 0:
        color = "#FFFFFF"
    elif int(val[-3:-1]) == 1:
        color = "#db9d9d"
    elif int(val[-3:-1]) == -1:
        color = '#abe5a8'
    elif int(val[-3:-1]) > -1:
        color = "#EC7063"
    else:
        color = "#52BE80"
    return 'background-color: %s' % color

def get_team_id_from_team_name(team_name):
    """
    Function finds team id in team dictionary from team name.
    @param team_name: name of Yahoo Fantasy team
    @return: id of Yahoo Fantasy team
    """
    return "".join([x[TEAM_KEY] for x in league_team_list if x[NAME_KEY] == team_name])

def team_player_list(team_id):
    """
    Function returns Yahoo Fantasy player names that are actively rostered in a team id.
    @param team_id: id of Yahoo Fantasy team
    @return: list of rostered players
    """
    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    team = league.to_team(team_id)
    team_roster = team.roster()
    player_in_team_list = [player[NAME_KEY] for player in team_roster]
    return player_in_team_list

def streamlit_return_players_on_team(team_name):
    """
    Streamlit function to return sorted player names rostered by team with a team name argument.
    @param team_name: name of Yahoo Fantasy team
    @return: sorted list of rostered players
    """
    team_id = get_team_id_from_team_name(team_name)
    player_list = team_player_list(team_id)
    player_list = sorted(player_list)
    return player_list

@st.cache(show_spinner=False)
def get_league_free_agents():
    """
    Function queries the Yahoo Fantasy API to return a list of the leagues current free agents (FA).
    @return: sorted list of free agents
    """
    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    free_agent_guards = league.free_agents("G")
    free_agent_forwards = league.free_agents("F")
    free_agent_centers = league.free_agents("C")
    free_agents = [player[NAME_KEY] for player in free_agent_guards] \
        + [player[NAME_KEY] for player in free_agent_forwards] \
        + [player[NAME_KEY] for player in free_agent_centers]
    free_agents = list(set(free_agents))
    sorted_free_agents = sorted(free_agents)
    return sorted_free_agents

@st.cache(show_spinner=False)
def get_team_roster_stats_dataframe(team_dict):
    """
    Function returns a dataframe with a desired teams players season average 9cat stats
    @param team_dict: dictionary containing team information from league
    @return: team roster season average 9cat stats dataframe
    """
    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    team_9cat_stats = team_9cat_average_stats(team_dict, league)
    return team_9cat_stats

@st.cache(show_spinner=False, allow_output_mutation=True)
def streamlit_waiver_add_and_drop(current_9cat_roster_averages, player_to_drop, player_to_add):

    team_players_9cat_stats_dataframe = current_9cat_roster_averages
    current_team_9cat_average_stats = pd.DataFrame(team_players_9cat_stats_dataframe
                                                   .loc[MEAN_ROW]).T.drop(PLAYER_COLUMN, axis=1)

    removed_mean_dropped_player_dataframe = remove_mean_and_player\
        (team_players_9cat_stats_dataframe, player_to_drop)

    added_player_9cat_averages = p9ca.get_player_9cat_season_average(player_to_add)
    new_team_9cat_average_stats_dataframe = removed_mean_dropped_player_dataframe.append\
        (added_player_9cat_averages)
    new_team_9cat_average_stats_dataframe.reset_index(inplace=True, drop=True)

    new_team_9cat_average_stats_dataframe = format_roster_dataframe \
        (new_team_9cat_average_stats_dataframe)

    new_team_9cat_average_stats = pd.DataFrame(new_team_9cat_average_stats_dataframe
                                                   .loc[MEAN_ROW]).T.drop(PLAYER_COLUMN, axis=1)

    difference_team_9cat_averages = drop_add_mean_9cat_difference(current_team_9cat_average_stats,
                                              new_team_9cat_average_stats)

    return team_players_9cat_stats_dataframe, current_team_9cat_average_stats, \
           new_team_9cat_average_stats_dataframe, new_team_9cat_average_stats, \
           difference_team_9cat_averages

def get_overall_power_rank(power_ranking_dataframe):
    """
    Function finds the Power Rankings for each team in the dataframe by adding each rows column
    positions and subtracting total from 109. Max PR score is 100.
    @param power_ranking_dataframe: dataframe with columns scored by their respective row standings
    @return: dataframe with columns scored by their respective row standings plus overall PR column
    """
    power_ranking_dataframe = power_ranking_dataframe.set_index(TEAM_COLUMN)
    power_ranking_dataframe[PR_COLUMN] = 109 - power_ranking_dataframe.sum(axis=1,
                                                                           numeric_only=True)
    columns = list(power_ranking_dataframe.columns)
    columns = [columns[-1]] + columns[:-1]
    power_ranking_dataframe = power_ranking_dataframe[columns]
    power_ranking_dataframe = power_ranking_dataframe.sort_values(PR_COLUMN, ascending=False)
    return power_ranking_dataframe

def clean_league_averages_dataframe(league_averages_dataframe):

    league_averages_dataframe_sorted = league_averages_dataframe.sort_values(TEAM_COLUMN,
                                                                             ascending=True)
    league_averages_dataframe_index = league_averages_dataframe_sorted.set_index(TEAM_COLUMN)
    return league_averages_dataframe_index


# Final averages/power_ranking/change
def columns_to_string(new_league_averages_dataframe, new_league_power_rankings,
                      power_rankings_difference):
    """

    @param new_league_averages_dataframe:
    @param new_league_power_rankings:
    @param power_rankings_difference:
    @return:
    """
    overall_power_rank_dataframe = pd.DataFrame()
    overall_power_rank_dataframe[TEAM_COLUMN] = new_league_averages_dataframe[TEAM_COLUMN]
    for column in new_league_averages_dataframe.columns[1:]:
        overall_power_rank_dataframe[column] = \
            new_league_averages_dataframe[column].astype(str) + " [" + new_league_power_rankings[
            column + " "].astype(str) + ", " + power_rankings_difference[column + " "].astype(
                str) + "]"
    return overall_power_rank_dataframe


def format_overall_power_rankings(unformatted_overall_power_rankings):

    formatted_overall_power_rankings = unformatted_overall_power_rankings.copy()
    for column in formatted_overall_power_rankings.columns[1:]:
        temporary_column_list = list()
        if column == "FG_PCT" or column == "FT_PCT" or column == "PTS":
            for value in formatted_overall_power_rankings[column]:
                if value[4] == " ":
                    value = value[:4] + "0 " + value[5:]
                    temporary_column_list.append(value)
                else:
                    temporary_column_list.append(value)
        else:
            for value in formatted_overall_power_rankings[column]:
                if value[3] == " ":
                    value = value[:3] + "0 " + value[4:]
                    temporary_column_list.append(value)
                else:
                    temporary_column_list.append(value)

        formatted_overall_power_rankings[column] = temporary_column_list

    return formatted_overall_power_rankings


def get_overall_power_rank_to_different_dataframe(power_ranking_dataframe, dataframe_to_add_to):

    power_ranking_dataframe = power_ranking_dataframe.set_index(TEAM_COLUMN)
    power_ranking_dataframe["PR"] = 109 - power_ranking_dataframe.sum(axis=1,  numeric_only=True)

    dataframe_to_add_to["PR"] = list(power_ranking_dataframe["PR"])

    columns = list(dataframe_to_add_to.columns)
    columns = [columns[-1]] + columns[:-1]
    dataframe_to_add_to = dataframe_to_add_to[columns]
    dataframe_to_add_to = dataframe_to_add_to.sort_values("PR", ascending=False)
    dataframe_to_add_to = dataframe_to_add_to.set_index(TEAM_COLUMN)
    dataframe_to_add_to.index.name = None

    return dataframe_to_add_to


def get_average_and_power_ranking_change(league_averages_dataframe, team_dict,
                                         new_team_9cat_averages):

    new_league_averages_dataframe, new_league_power_rankings, power_rankings_difference = \
        power_ranking_change(league_averages_dataframe, team_dict, new_team_9cat_averages)

    new_league_averages_dataframe = new_league_averages_dataframe.reset_index(drop=True)
    unformatted_overall_power_rankings = columns_to_string(new_league_averages_dataframe,
                                                           new_league_power_rankings,
                                                           power_rankings_difference)
    format_overall_power_dataframe = format_overall_power_rankings(unformatted_overall_power_rankings)
    returned_dataframe = get_overall_power_rank_to_different_dataframe(new_league_power_rankings,
                                                   format_overall_power_dataframe)
    return returned_dataframe

def columns_to_dtype_float(dataframe):
    """
    Converts dataframe columns to dtype float.
    param dataframe (pandas dataframe): dataframe to change column types
    returns dataframe (pandas dataframe): dataframe with changed column types
    """
    for column in dataframe.columns:
        try:
            dataframe[column] = dataframe[column].astype(float)
        except ValueError:
            pass
    return dataframe

def get_and_format_team_9cat(team, league):
    """
    Function first finds the teams 9cat averages by calling the *team_9cat_average_stats*
    function. It then filters to find the team mean and cleans and formats this single row
    dataframe. It changes the dtype of the columns to be floats.
    param team (dictionary): team dictionary
    param league (yahoo oauth object): yahoo authentication object
    returns team_9cat (dataframe): dataframe of team average 9cats
    """
    team_9cat = af.team_9cat_average_stats(team, league)
    team_9cat = team_9cat.loc[MEAN_ROW]
    team_9cat[PLAYER_COLUMN] = team[NAME_KEY]
    team_9cat = pd.DataFrame(team_9cat).T
    team_9cat.drop(PLAYER_COLUMN, inplace=True, axis=1)
    team_9cat = columns_to_dtype_float(team_9cat)
    return team_9cat

def applymap_color_and_format(dataframe):
    """
    Function takes a dataframe containing 9cat stat columns and returns a color coded and decimal
    place formatted dataframe for visual ease.
    param dataframe (pandas dataframe): dataframe to format
    returns dataframe (pandas dataframe): dataframe with formatted and colored values
    """
    colored_matchup_difference = dataframe.style.applymap(
        af.color_negative_red, subset=pd.IndexSlice[:,[af.FIELD_GOAL_PERCENTAGE_COLUMN,
                                                       af.FREE_THROW_PERCENTAGE_COLUMN,
                                                       af.THREES_MADE_COLUMN, af.POINTS_COLUMN,
                                                       af.REBOUNDS_COLUMN, af.ASSITS_COLUMN,
                                                       af.STEALS_COLUMN, af.BLOCKS_COLUMN
                                                       ]]).applymap(
        af.color_negative_red_tov, subset=pd.IndexSlice[:,[af.TURNOVERS_COLUMN]]).format\
        (COLUMN_9CAT_DECIMAL_FORMAT)
    return colored_matchup_difference

def compare_h2h_team_9cat(team1, team2):
    """
    Function authenticates on Yahoo and creates creates two dataframes containing team roster
    9cat averages for each team specified in the parameters. It calculates the difference between
    both 9cat averages and finally it formats the values for visual ease.
    params team1 (dictionary): team dictionary
    params team2 (dictionary): team dictionary
    return matchup_difference (dataframe): team difference 9cat dataframe
    return colored_matchup_difference (dataframe): formatted team difference 9cat dataframe
    """
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    team1_9cat_stats = get_and_format_team_9cat(team1, league)
    team2_9cat_stats = get_and_format_team_9cat(team2, league)
    matchup_difference = team1_9cat_stats.sub(team2_9cat_stats)
    colored_matchup_difference = applymap_color_and_format(matchup_difference)
    return matchup_difference, colored_matchup_difference

def get_game_information_in_month(nba_json):
    """
    Function loops through a month (n) in nba_json and creates a dataframe containing game
    information, game_id, home/visitor team/team_id and game_date for each month.
    param nba_json (dictionary): dictionary containing game information
    returns game_dataframe (pandas dataframe): dataframe containing game information for a month
    """
    game_dataframe = pd.DataFrame()
    for n in range(len(nba_json)):
        game_dictionary = dict()
        game_dictionary[GID_KEY] = nba_json[n][GID_KEY]
        game_dictionary[GDATE_KEY] = nba_json[n][GDATE_KEY]
        game_dictionary[VISITORS_TEAM_ID_KEY] = nba_json[n][V_KEY][TID_KEY]
        game_dictionary[VISITORS_KEY] = nba_json[n][V_KEY][TC_KEY] + " " \
                                        + nba_json[n][V_KEY][TN_KEY]
        game_dictionary[HOME_TEAM_ID_KEY] = nba_json[n][H_KEY][TID_KEY]
        game_dictionary[HOME_KEY] = nba_json[n][H_KEY][TC_KEY] + " " \
                                    + nba_json[n][H_KEY][TN_KEY]
        game_dataframe = game_dataframe.append(game_dictionary, ignore_index=True)
    return game_dataframe

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_game_information_in_season(season):
    """
    Function calls the NBA endpoint that returns the season schedule. It then loops through each
    month in that schedule to create a dataframe containing game information, game_id,
    home/visitor team/team_id and game_date for the season.
    param season (string): season for schedule
    returns season_games_dataframe (pandas dataframe): dataframe containing game information for
    a season
    """
    r = requests.get(f"http://data.nba"
                     f".com/data/10s/v2015/json/mobile_teams/nba/{season}/league/00_full_schedule"
                     f".json")
    game_information_json = r.json()[LSCD_KEY]
    season_games_dataframe = pd.DataFrame()
    for n in range(len(game_information_json)):
        month_n_game_dataframe = get_game_information_in_month\
            (game_information_json[n][MSCD_KEY][G_KEY])
        season_games_dataframe = season_games_dataframe.append(month_n_game_dataframe)
    return season_games_dataframe

def get_week_current_week_information():
    """
    Function finds the current Yahoo Fantasy week number and its start and end date.
    return current_fantasy_week (int): Yahoo Fantasy week number
    return week_start_date (string): start date of Yahoo Fantasy week number
    return week_end_date (string): end date of Yahoo Fantasy week number
    """
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    current_fantasy_week = league.current_week()
    week_start_date = league.week_date_range(current_fantasy_week)[0]
    week_end_date = league.week_date_range(current_fantasy_week)[1]
    return current_fantasy_week, week_start_date, week_end_date

def get_next_week_information():
    """
    Function finds the next Yahoo Fantasy week number and its start and end date.
    return next_fantasy_week (int): Yahoo Fantasy week number
    return week_start_date (string): start date of Yahoo Fantasy week number
    return week_end_date (string): end date of Yahoo Fantasy week number
    """
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    next_fantasy_week = league.current_week() + 1
    week_start_date = league.week_date_range(next_fantasy_week)[0]
    week_end_date = league.week_date_range(next_fantasy_week)[1]
    return next_fantasy_week, week_start_date, week_end_date

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_player_ids_names_in_fantasy_team(team_dict):
    """
    Function finds the Yahoo Fantasy player ids and player names rostered by a team in the league
    param team_dict (dictionary): dictionary containing information about a owners team
    return player_id_name_team_list (list): Yahoo Fantasy player ids and names
    return player_name_list (list): Yahoo Fantasy player names
    """
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    team = league.to_team(team_dict[TEAM_KEY])
    team_roster = team.roster()
    player_id_name_team_list = [{PLAYER_ID_KEY : player[PLAYER_ID_KEY], NAME_KEY : player[NAME_KEY]}
                           for player in team_roster]
    player_name_list = [player[NAME_KEY] for player in player_id_name_team_list]
    return player_id_name_team_list, player_name_list

def get_fantasy_week_games_dataframe(season_schedule_dataframe, week_start_date, week_end_date):
    """
    Function filters the entire NBA season schedule on a start/end date to find the scheduled
    games between specific dates. It returns the amount of games each NBA team plays during that
    period of time.
    param season_schedule_dataframe (pandas dataframe): dataframe containing the entire seasons
    NBA schedule
    param week_start_date (string): date to begin filtering by
    param week_start_date (string): date to end filtering by
    return current_fantasy_games_week (pandas dataframe) dataframe containing the scheduled games
    in specified param dates
    return team_game_counts (pandas series): series containing count of games for each NBA team
    """
    filtered_games_week = season_schedule_dataframe[(season_schedule_dataframe[GDATE_KEY] >=
                                                   str(week_start_date)) &
                                                  (season_schedule_dataframe[GDATE_KEY] <=
                                                   str(week_end_date))]
    team_game_counts = filtered_games_week[HOME_KEY].append\
        (filtered_games_week[VISITORS_KEY]).value_counts()
    return filtered_games_week, team_game_counts

def get_player_games(team_game_counts_series, player_name_list):
    """
    Function creates a dictionary containing key/value pairs of player names/games in a series of
    NBA team game counts
    param team_game_counts_series (pandas series): series of team name and games playing
    param player_name_list (list): list of player names
    return player_games_dictionary (dictionary): key/value pairing of player names/games playing
    """
    player_games_dictionary = dict()
    team_game_counts_dataframe = pd.DataFrame(team_game_counts_series)
    team_game_counts_dataframe.reset_index(inplace=True)
    team_game_counts_dataframe = team_game_counts_dataframe.replace(NBA_NAME_LA_CLIPPERS,
                                                                    YAHOO_NAME_LA_CLIPPERS)
    for player in player_name_list:
        team = af.yahoo_player_team_and_jersey(player)[0]
        player_games_dictionary[player] = \
            team_game_counts_dataframe[team_game_counts_dataframe[INDEX_COLUMN] == team][0].iloc[0]
    return player_games_dictionary

def get_predicted_player_weekly_9cat(player_games_dictionary, team_9cat_average_stats):
    """
    Function is used to create a dataframe which contains predicted totals for a week of Yahoo
    Fantasy play. For each player, 9cat features are multiplied by the amount of games that
    player plays in one week.
    param player_games_dictionary (dictionary): key/value pairing of player names/games playing
    param team_9cat_average_stats (pandas dataframe): dataframe containing the season average
    9cat stats for each player on a team
    return predicted_9cat_stats (pandas dataframe): dataframe with 9cat averages multiplied by
    games played in a week
    """
    predicted_9cat_stats = pd.DataFrame()
    team_9cat_average_stats = columns_to_dtype_float(team_9cat_average_stats)
    for player in player_games_dictionary.keys():
        player_predicted_9cat_stats = pd.concat(
            [team_9cat_average_stats[team_9cat_average_stats[PLAYER_COLUMN] == player].iloc[:, :3],
            (team_9cat_average_stats[team_9cat_average_stats[PLAYER_COLUMN] == player].iloc[:, 3:]
            * 3)], axis=1)
        predicted_9cat_stats = player_predicted_9cat_stats.append(predicted_9cat_stats)
    predicted_9cat_stats.sort_index(inplace=True)
    return predicted_9cat_stats

def get_total_row(roster_dataframe):
    """
    Function creates a row in the provided parameter dataframe which contains the total for
    categories that should be summed and averages for categories that should be averaged
    param roster_dataframe (pandas dataframe): dataframe containing player week 9cat stats
    return roster_dataframe_with_total (pandas dataframe): dataframe containing total row
    """
    sum_9cat_column_dataframe = pd.DataFrame(roster_dataframe.iloc[:, 3:].sum()).T
    mean_9cat_column_dataframe =  pd.DataFrame(roster_dataframe.iloc[:, 1:3].mean()).T
    total_dataframe = pd.concat([mean_9cat_column_dataframe,  sum_9cat_column_dataframe], axis=1)
    total_dataframe[PLAYER_COLUMN] = TOTAL_ROW
    roster_dataframe_with_total = roster_dataframe.append(total_dataframe)
    roster_dataframe_with_total.reset_index(inplace=True, drop=True)
    return roster_dataframe_with_total

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_teams_weekly_predicted_stats_pipeline(team_dict, week="next", season=2020,
                                              team_9cat_average_stats_data=None):
    """
    Function pipelines the process required to find a league teams weekly predicted 9cat totals.
    Initially, the number of games for each player in the provided parameter week is found.
    Average 9cat player stats are multiplied by that number and the entire roster stats are
    summed to provide a total. The dataframe is finally formatted.
    param team_dict (dictionary): dictionary of team from league
    param week (string): determines which week to calculate weekly games for
    param season (int): determines which season to get NBA schedule for
    param team_9cat_average_stats_data (pandas dataframe): dataframe containing player 9cat season
    averages
    return roster_dataframe_with_total (pandas dataframe): dataframe containing player 9cat
    predicted weekly stats and entire roster totals
    """
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    if week == "next":
        fantasy_week, week_start_date, week_end_date = get_next_week_information()
    elif week == "current":
        fantasy_week, week_start_date, week_end_date = get_week_current_week_information()
    else:
        raise ValueError("Parameter 'week' must be 'current' or 'next'.")
    season_games_dataframe = get_game_information_in_season(season)
    filtered_games_week, team_game_counts = get_fantasy_week_games_dataframe\
        (season_games_dataframe, week_start_date, week_end_date)
    player_id_name_team_list, player_name_list = get_player_ids_names_in_fantasy_team(team_dict)
    player_games_dictionary = get_player_games(team_game_counts, player_name_list)
    if team_9cat_average_stats_data is None:
        team_9cat_average_stats_dataframe = af.team_9cat_average_stats(team_dict, league)
        predicted_weekly_9cat_stats = get_predicted_player_weekly_9cat(player_games_dictionary,
                                                                 team_9cat_average_stats_dataframe)
    else:
        predicted_weekly_9cat_stats = get_predicted_player_weekly_9cat(player_games_dictionary,
                                                                 team_9cat_average_stats_data)
    roster_dataframe_with_total = get_total_row(predicted_weekly_9cat_stats)
    roster_dataframe_with_total = af.format_dataframe_decimals(roster_dataframe_with_total)
    return roster_dataframe_with_total

def get_filtered_total_row(total_dataframe, team_dict):
    """
    Function filters a dataframe containing weekly total 9cat stats and returns the *total* row
    so that it can be used for differencing. The function appends the team name to the total row
    param total_dataframe (pandas dataframe): dataframe containing weekly total 9cat stats
    param team_dict (dictionary): dictionary of team from league
    return total_row_dataframe (pandas dataframe): single row dataframe containing total 9cat
    stats with team name
    return total_row_dataframe_no_name (pandas dataframe): single row dataframe containing total 9cat
    stats without team name
    """
    total_row_dataframe = total_dataframe[total_dataframe[PLAYER_COLUMN] == TOTAL_ROW]
    total_row_dataframe[PLAYER_COLUMN] = team_dict[NAME_KEY]
    total_row_dataframe.index = [TOTAL_ROW]
    total_row_dataframe_no_name = total_row_dataframe.drop(PLAYER_COLUMN, axis=1)
    return total_row_dataframe, total_row_dataframe_no_name

@st.cache(allow_output_mutation=True, show_spinner=False)
def weekly_matchup_evaluator(team1_dict, team2_dict, team1_9cat_average_stats_data=None,
                             team2_9cat_average_stats_data=None, week="next", season=2020):
    """

    """
    team1_roster_dataframe_with_total = get_teams_weekly_predicted_stats_pipeline(
        team1_dict, week=week, season=season,
        team_9cat_average_stats_data=team1_9cat_average_stats_data)
    team2_roster_dataframe_with_total = get_teams_weekly_predicted_stats_pipeline(
        team2_dict, week=week, season=season,
        team_9cat_average_stats_data=team2_9cat_average_stats_data)
    team1_total_row_dataframe, team1_total_row_dataframe_no_name = get_filtered_total_row\
        (team1_roster_dataframe_with_total, team1_dict)
    team2_total_row_dataframe, team2_total_row_dataframe_no_name = get_filtered_total_row\
        (team2_roster_dataframe_with_total, team2_dict)
    team1_total_row_dataframe_no_name = columns_to_dtype_float(team1_total_row_dataframe_no_name)
    team2_total_row_dataframe_no_name = columns_to_dtype_float(team2_total_row_dataframe_no_name)
    total_difference_dataframe = team1_total_row_dataframe_no_name.subtract\
        (team2_total_row_dataframe_no_name)
    total_difference_dataframe_colored = applymap_color_and_format(total_difference_dataframe)
    return total_difference_dataframe, total_difference_dataframe_colored

def get_teams_matchup_number(team_dict, matchups):
    """
    Function loops through returned the returned Yahoo Fantasy matchup nested dictionary to find
    the matchup number of the specified parameter team name.
    param team_dict (dictionary): dictionary containing information about a owners team
    param matchups (dictionary): league matchup information from specified week number
    return matchup (string): string value for the index of the specified teams nested matchup
    dictionary in the original matchup dictionary
    """
    for matchup in range(len(matchups[FANTASY_CONTENT_KEY][LEAGUE_KEY][1][SCOREBOARD_KEY][ZERO_KEY]\
                [MATCHUPS_KEY]) - 1):
        if matchups[FANTASY_CONTENT_KEY][LEAGUE_KEY][1][SCOREBOARD_KEY][ZERO_KEY]\
                [MATCHUPS_KEY][str(matchup)][MATCHUP_KEY][ZERO_KEY][TEAMS_KEY][ZERO_KEY]\
                [TEAM_KEY_2][0][2][NAME_KEY] == team_dict[NAME_KEY] \
                or matchups[FANTASY_CONTENT_KEY][LEAGUE_KEY][1][SCOREBOARD_KEY][ZERO_KEY]\
                [MATCHUPS_KEY][str(matchup)][MATCHUP_KEY][ZERO_KEY][TEAMS_KEY][ONE_KEY]\
                [TEAM_KEY_2][0][2][NAME_KEY] == team_dict[NAME_KEY]:
            return str(matchup)

def get_team_name_from_matchup(matchups, matchup_number, matchup_team_number):
    """
    Function returns the team name in a matchup.
    param matchups (dictionary): league matchup information from specified week number
    param matchup_number (string): matchup number for in matchups dictionary
    param matchup_team_number (string): either "0" or "1" indicating matchup team number
    return team_name (string): name of team in matchup
    """
    team_name = matchups[FANTASY_CONTENT_KEY][LEAGUE_KEY][1][SCOREBOARD_KEY][ZERO_KEY]\
                [MATCHUPS_KEY][matchup_number][MATCHUP_KEY][ZERO_KEY][TEAMS_KEY]\
                [matchup_team_number][TEAM_KEY_2][0][2][NAME_KEY]
    return team_name

def get_live_matchup_stats_dictionary(matchups, matchup_number, matchup_team_number):
    """
    Function returns a dictionary containing 9cat stats plus two more for a given matchup and
    matchup team number.
    param matchups (dictionary): league matchup information from specified week number
    param matchup_number (string): matchup number for in matchups dictionary
    param matchup_team_number (string): either "0" or "1" indicating matchup team number
    return live_matchup_stats (dictionary): dictionary of 9cat stats plus two more stats
    """
    live_matchup_stats = matchups[FANTASY_CONTENT_KEY][LEAGUE_KEY][1][SCOREBOARD_KEY][ZERO_KEY]\
                [MATCHUPS_KEY][matchup_number][MATCHUP_KEY][ZERO_KEY][TEAMS_KEY]\
                [matchup_team_number][TEAM_KEY_2][1][TEAM_STATS_KEY][STATS_KEY]
    return live_matchup_stats

def get_dataframe_from_live_matchup_stats(matchup_stats_dictionary, team_name):
    """
    Function creates a 1x10 dataframe containing the name of the team along with this live 9cat
    stats for a weeks matchup.
    param matchup_stats_dictionary (dictionary): dictionary containing the stats for a team
    param team_name (string): the name of the team
    return live_matchup_9cat_stats_dataframe (pandas dataframe): dataframe containing the name of the team along with this live 9cat
    stats for a weeks matchup
    """
    matchup_9cat_stats_list = list()
    for index in range(len(matchup_stats_dictionary)):
        if index != 0 and index != 2:
            matchup_9cat_stats_list.append(matchup_stats_dictionary[index][STAT_KEY][VALUE_KEY])
    values = [team_name] + matchup_9cat_stats_list
    live_matchup_9cat_stats_dataframe = pd.DataFrame(values).T
    live_matchup_9cat_stats_dataframe.columns = MATCHUP_COLUMNS
    live_matchup_9cat_stats_dataframe = live_matchup_9cat_stats_dataframe.replace("", 0)
    return live_matchup_9cat_stats_dataframe


def applymap_color_and_format(dataframe):
    """
    Function takes a dataframe containing 9cat stat columns differneces and returns a color coded
    and decimal place formatted dataframe for visual ease.
    param dataframe (pandas dataframe): dataframe to format
    returns dataframe (pandas dataframe): dataframe with formatted and colored values
    """
    colored_matchup_difference = dataframe.style.applymap(
        af.color_negative_red, subset=pd.IndexSlice[:,[af.FIELD_GOAL_PERCENTAGE_COLUMN,
                                                       af.FREE_THROW_PERCENTAGE_COLUMN,
                                                       af.THREES_MADE_COLUMN, af.POINTS_COLUMN,
                                                       af.REBOUNDS_COLUMN, af.ASSITS_COLUMN,
                                                       af.STEALS_COLUMN, af.BLOCKS_COLUMN
                                                       ]]).applymap(
        af.color_negative_red_tov, subset=pd.IndexSlice[:,[af.TURNOVERS_COLUMN]]).format\
        (COLUMN_9CAT_DECIMAL_FORMAT)
    return colored_matchup_difference

def format_3ptm_to_tov_as_int(dataframe):
    """
    Function changes the 3ptm to tov columns to dtype int needed for the live score dataframes.
    @param dataframe: dataframe with columns to convert
    @return: converted dataframe
    """
    for column in dataframe.columns[2:]:
        dataframe[column] = dataframe[column].astype(int)
    return dataframe


def get_matchup_teams_9cat_stat_dataframes(week, team_dict):
    """

    @param week:
    @type week:
    @param team_dict:
    @type team_dict:
    @return:
    @rtype:
    """
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    matchups = league.matchups(week=week)
    matchup_number = get_teams_matchup_number(team_dict, matchups)
    first_team_name = get_team_name_from_matchup(matchups, matchup_number, "0")
    second_team_name = get_team_name_from_matchup(matchups, matchup_number, "1")
    first_team_stats_dictionary = get_live_matchup_stats_dictionary(matchups, matchup_number,
                                                                    "0")
    second_team_stats_dictionary = get_live_matchup_stats_dictionary(matchups, matchup_number,
                                                                     "1")
    first_team_stats_dataframe = get_dataframe_from_live_matchup_stats(first_team_stats_dictionary,
                                                              first_team_name)
    first_team_stats_dataframe = first_team_stats_dataframe.set_index(PLAYER_COLUMN)
    second_team_stats_dataframe = get_dataframe_from_live_matchup_stats(second_team_stats_dictionary,
                                                              second_team_name)
    second_team_stats_dataframe = second_team_stats_dataframe.set_index(PLAYER_COLUMN)
    matchup_stats_dataframe = first_team_stats_dataframe.append(second_team_stats_dataframe)
    matchup_stats_dataframe = remove_player_and_float_convert(matchup_stats_dataframe)
    matchup_stats_dataframe = format_3ptm_to_tov_as_int(matchup_stats_dataframe)
    return first_team_name, first_team_stats_dataframe, second_team_name, \
           second_team_stats_dataframe, matchup_stats_dataframe

def get_team_predicted_stats_dataframe(team_name, schedule_dataframe, week_start_date,
                                       week_end_date):
    """
    Function creates a dataframe containing the predicted 9cat stats for a teams roster dependent
    on the amount of games each player has left to play in the stated date range.
    @param team_name (string): name of Yahoo Fantasy team
    @param schedule_dataframe (pandas dataframe): dataframe containing the entire seasons
    NBA schedule
    @param week_start_date (string): start date of to begin schedule_dataframe filtering
    @param week_end_date (string): endd date of to begin schedule_dataframe filtering
    @return predicted_stats_dataframe: predicted 9cat stats for a teams roster
    @return team_dictionary (dictionary): dictionary of team from league
    """
    team_dictionary = get_team_dict_from_team_name(team_name)
    name_id_dictionary, name_list = get_player_ids_names_in_fantasy_team(team_dictionary)
    games_left_dataframe, games_left_series = get_fantasy_week_games_dataframe\
        (schedule_dataframe, week_start_date, week_end_date)
    player_game_dictionary = get_player_games(games_left_series, name_list)
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    team_9cat_average_stats_dataframe = af.team_9cat_average_stats(team_dictionary, league)
    predicted_stats_dataframe = get_predicted_player_weekly_9cat(player_game_dictionary,
                                                                team_9cat_average_stats_dataframe)
    return predicted_stats_dataframe, team_dictionary

def get_clean_predicted_stats_dataframe(predicted_stats_dataframe, team_dict):
    """
    Function cleans the predicted stats dataframe by creating a total row and adding the name of
    the team via the team_dict parameter.
    @param predicted_stats_dataframe (pandas dataframe): predicted 9cat stats for a teams roster
    @param team_dict (dictionary): dictionary of team from league
    @return total_row_predicted_stats_datafame: 1x10 predicted 9cat dataframes
    @return total_row_predicted_stats_datafame_no_name: 1x9 predicted 9cat dataframes (without
    team name)
    """
    dataframe_with_total = get_total_row(predicted_stats_dataframe)
    total_row_predicted_stats_datafame, total_row_predicted_stats_datafame_no_name = \
        get_filtered_total_row(dataframe_with_total, team_dict)
    return total_row_predicted_stats_datafame, total_row_predicted_stats_datafame_no_name

def add_live_stats_and_predicted_dataframes(live_stats_dataframe,
                                            total_row_predicted_stats_datafame, team_name):
    """
    Function adds the dataframes containing live matchup stats and the predicted game stats. It
    returns a 1x10 dataframe with team name and 9cat stats.
    @param live_stats_dataframe (pandas dataframe): current matchup 9cat stats for a team roster
    @param total_row_predicted_stats_datafame (pandas dataframe): total row predicted 9cat stats
    for a team roster
    @param team_name (string): name of Yahoo Fantasy team
    @return live_plus_prediction_dataframe: 1X10 9cat live plus predicted 9cat stats dataframe
    """
    total_row_predicted_stats_datafame.reset_index(inplace=True, drop=True)
    live_stats_dataframe = columns_to_dtype_float(live_stats_dataframe)
    # live_stats_dataframe.drop(PLAYER_COLUMN, axis=1, inplace=True)
    total_row_predicted_stats_datafame.drop(PLAYER_COLUMN, axis=1, inplace=True)
    live_plus_prediction_dataframe = live_stats_dataframe.add(total_row_predicted_stats_datafame)
    temporary_dataframe = pd.DataFrame()
    temporary_dataframe[PLAYER_COLUMN] = team_name
    live_plus_prediction_dataframe = pd.concat([temporary_dataframe,
                                                live_plus_prediction_dataframe])
    live_plus_prediction_dataframe[PLAYER_COLUMN] = team_name
    return live_plus_prediction_dataframe

@st.cache(allow_output_mutation=True, show_spinner=False)
def live_plus_prediction_matchup_dataframe(schedule_dataframe, team_name, current_date,
                                           week_end_date):
    """

    @param schedule_dataframe:
    @param team_name:
    @param current_date:
    @param week_end_date:
    @return:
    """
    predicted_stats_dataframe, team_dictionary = get_team_predicted_stats_dataframe \
        (team_name, schedule_dataframe, current_date, week_end_date)
    total_row_predicted_stats_datafame, total_row_predicted_stats_datafame_no_name = \
        get_clean_predicted_stats_dataframe(predicted_stats_dataframe, team_dictionary)
    live_plus_prediction_dataframe = add_live_stats_and_predicted_dataframes(team1_live_stats,
                                                                             total_row_predicted_stats_datafame,
                                                                             team_name)
    return live_plus_prediction_dataframe


def get_team_dict_from_team_name(team_name):
    """
    Function returns the team dictionary from a team name.
    @param team_name: name of fantasy team
    @type team_name: string
    @return: dictionary of fantasy team
    @rtype: dictionary
    """
    if team_name == af.AUTOPICK[NAME_KEY]:
        team_dict = af.AUTOPICK
    elif team_name == af.CRABBEHERBYTHEPUSSY[NAME_KEY]:
        team_dict = af.CRABBEHERBYTHEPUSSY
    elif team_name == af.EL_LADRON_DE_CABRAS[NAME_KEY]:
        team_dict = af.EL_LADRON_DE_CABRAS
    elif team_name == af.LALALAND[NAME_KEY]:
        team_dict = af.LALALAND
    elif team_name == af.MAGICS_JOHNSON[NAME_KEY]:
        team_dict = af.MAGICS_JOHNSON
    elif team_name == af.MCCURRY[NAME_KEY]:
        team_dict = af.MCCURRY
    elif team_name == af.NUNN_OF_YALL_BETTA[NAME_KEY]:
        team_dict = af.NUNN_OF_YALL_BETTA
    elif team_name == af.RUSTY_CUNTBROOKS[NAME_KEY]:
        team_dict = af.RUSTY_CUNTBROOKS
    elif team_name == af.SWAGGY_P[NAME_KEY]:
        team_dict = af.SWAGGY_P
    elif team_name == af.TVONS_TIP_TOP_TEAM[NAME_KEY]:
        team_dict = af.TVONS_TIP_TOP_TEAM
    elif team_name == af.WAKANDA_FOREVER[NAME_KEY]:
        team_dict = af.WAKANDA_FOREVER
    elif team_name == af.YOBITCH_TOPPIN_ME[NAME_KEY]:
        team_dict = af.YOBITCH_TOPPIN_ME
    return team_dict

def move_column_inplace(df, col, pos):
    col = df.pop(col)
    df.insert(pos, col.name, col)

def get_winning_cats(matchup_stats_dataframe):
    """
    Function counts, for each team (row) in dataframe, which team has better category values.
    This provides a score informing total categories that each team is winning.
    @param matchup_stats_dataframe:
    @return: dataframe with category win count column
    """
    count_team1_win_list = 0
    count_team2_win_list = 0
    for column in matchup_stats_dataframe.columns[:-1]:
        if matchup_stats_dataframe[column][0] > matchup_stats_dataframe[column][1]:
            count_team1_win_list += 1
        elif matchup_stats_dataframe[column][0] < matchup_stats_dataframe[column][1]:
            count_team2_win_list += 1
        else:
            pass
    if matchup_stats_dataframe[TURNOVERS_COLUMN][0] > matchup_stats_dataframe[TURNOVERS_COLUMN][1]:
        count_team2_win_list += 1
    elif matchup_stats_dataframe[TURNOVERS_COLUMN][0] < matchup_stats_dataframe[TURNOVERS_COLUMN][1]:
        count_team1_win_list += 1
    else:
        pass
    team_stat_win_list = [count_team1_win_list, count_team2_win_list]
    matchup_stats_dataframe[CATS_COLUMNS] = team_stat_win_list
    move_column_inplace(matchup_stats_dataframe, CATS_COLUMNS, 0)
    return matchup_stats_dataframe

def get_live_matchup_stats_pipeline(team_dictionary):
    """
    Function pipelines the process involved in returning, for a specified team, its matchups
    live stats and category win columns count
    @param team_dictionary: dictionary containing team information from league
    @return: dataframe with live matchup 9cat stats and category win count column
    """
    current_fantasy_week, week_start_date, week_end_date = get_week_current_week_information()
    team1_name, team1_live_stats, team2_name, team2_live_stats, matchup_stats_dataframe = \
        get_matchup_teams_9cat_stat_dataframes(current_fantasy_week, team_dictionary)
    matchup_stats_dataframe = get_winning_cats(matchup_stats_dataframe)
    return current_fantasy_week, team1_name, team1_live_stats, team2_name, team2_live_stats, \
           matchup_stats_dataframe

# Wide mode
def _max_width_():
    """
    Function sets width for Streamlit app
    @return: None
    """
    max_width_str = f"max-width: 1350px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

def highlight_max(s):
    is_large = s.nlargest(1).values
    return ['font-weight: bold' if v in is_large else '' for v in s]


def combine_current_new_differnce_dataframes_player_transaction(current_team_9cat_averages,
                                                                new_team_9cat_averages,
                                                                difference_team_9cat_averages):
    """

    @param current_team_9cat_averages:
    @param new_team_9cat_averages:
    @param difference_team_9cat_averages:
    @return:
    """
    current_team_9cat_averages[""] = CURRENT_COLUMN
    new_team_9cat_averages[""] = NEW_COLUMN
    difference_team_9cat_averages[""] = DIFFERENCE_COLUMN
    formatted_current_team_9cat_averages = current_team_9cat_averages.set_index("")
    formatted_new_team_9cat_averages = new_team_9cat_averages.set_index("")
    formatted_difference_team_9cat_averages = difference_team_9cat_averages.set_index("")
    transaction_dataframe = pd.concat([formatted_current_team_9cat_averages,
                                       formatted_new_team_9cat_averages,
                                       formatted_difference_team_9cat_averages], axis=0)
    return transaction_dataframe


def get_teams_league_standing(team_name):
    """
    Function returns a teams current league standing
    @param team_name: name of Yahoo Fantasy team
    @return: current league standing
    """
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    league_standings_dictionary = league.standings()
    standing = "".join([x[RANK_KEY] for x in league_standings_dictionary if x[NAME_KEY] ==
                        team_name])
    return standing

def format_team_standing_string(standing):
    """
    Function formats standing so it can be used in a sentence
    @param standing: current league standing
    @return: formatted standing
    """
    if standing == "1":
        return standing + "st"
    elif standing == "2":
        return standing + "nd"
    else:
        return standing + "th"

def get_team_names_from_matchup_week(week, team_dict):
    """
    Function returns both team names from a specified week and team name matchup
    @param week: week number
    @param team_dict: team information dictionary
    @return: names of both teams in matchup
    """
    sc = af.yahoo_fantasy_api_authentication()
    league = af.yahoo_fantasy_league(sc)
    matchups = league.matchups(week=week)
    matchup_number = get_teams_matchup_number(team_dict, matchups)
    first_team_name = get_team_name_from_matchup(matchups, matchup_number, "0")
    second_team_name = get_team_name_from_matchup(matchups, matchup_number, "1")
    return first_team_name, second_team_name

# Force load in wide mode
_max_width_()

# Streamlit App start
# Header/Title


# Live standings
team = st.sidebar.selectbox(
     'Lebrontourage Teams',
     ("Select a Team", AUTOPICK[NAME_KEY], CRABBEHERBYTHEPUSSY[NAME_KEY],
      EL_LADRON_DE_CABRAS[NAME_KEY], LALALAND[NAME_KEY], MAGICS_JOHNSON[NAME_KEY],
      MCCURRY[NAME_KEY], NUNN_OF_YALL_BETTA[NAME_KEY], RUSTY_CUNTBROOKS[NAME_KEY],
      SWAGGY_P[NAME_KEY], TVONS_TIP_TOP_TEAM[NAME_KEY], WAKANDA_FOREVER[NAME_KEY],
      YOBITCH_TOPPIN_ME[NAME_KEY]), 7, key="team2")
if team not in LEAGUE_TEAM_NAMES:
    st.warning('Select a team...')
    st.stop()
live_standings_team_dict = get_team_dict_from_team_name(team)
current_fantasy_week, team1_name, team1_live_stats, team2_name, team2_live_stats, \
    live_matchup_stats_dataframe = get_live_matchup_stats_pipeline(live_standings_team_dict)
team1_name_standing = get_teams_league_standing(team1_name)
team2_name_standing = get_teams_league_standing(team2_name)

#
st.subheader('Matchup')
st.write(f"The live scores for the week {current_fantasy_week} matchup between {team1_name} "
         f"({format_team_standing_string(team1_name_standing)}) and {team2_name} "
         f"({format_team_standing_string(team2_name_standing)}) are...")
st.table(live_matchup_stats_dataframe.style.highlight_min(subset=["TOV"], color='#f0f0f0',
                                                          axis=0).highlight_max(subset=["CATS",
    "FG_PCT", "FT_PCT", "FG3M", "PTS", "REB", "AST", "STL", "BLK"], color='#f0f0f0', axis=0).format(
    STREAMLIT_LIVE_SCORES_TABLE_FORMAT))

# Get next week matchup/team/standings information
next_fantasy_week = get_next_week_information()[0]
next_matchup_team1_name, next_matchup_team2_name = get_team_names_from_matchup_week(
    next_fantasy_week, live_standings_team_dict)
next_matchup_team1_name_standing = get_teams_league_standing(next_matchup_team1_name)
next_matchup_team2_name_standing = get_teams_league_standing(next_matchup_team2_name)

# Text about next week matchup/team/standings
st.write("")
st.write(f"The following week {next_fantasy_week} matchup is  between {next_matchup_team1_name} "
         f"({format_team_standing_string(next_matchup_team1_name_standing)}) and"
         f" {next_matchup_team2_name} "
         f"({format_team_standing_string(next_matchup_team2_name_standing)}).")


# Streamlit Code
st.subheader('Free Agent Machine')
st.write("This feature simulates a FA transaction and calculates your teams 9Cat averages "
         "before and after the pick-up. Use this tool to discover how a player add/drop transaction" 
         " impacts your teams average 9Cat stats. This process will take ~1 minute to run "
         "initially as it loads and calculates your entire teams 9cat stats. After its initial "
         "loading, select a player to drop and a player to add, the transaction information will be"
         " presented quickly.")
# st.write("Firstly, select your team. Secondly, select the player you want to drop. Thirdly, "
#          "select the FA you want to add. Compare!")
st.write("")
# Reference variables
team_dict = get_team_dict_from_team_name(team)
# Load team dataframe
with st.spinner(f"Getting {team} team information..."):
    team_9cat_stats = get_team_roster_stats_dataframe(team_dict)



# Section title
st.sidebar.write("")
st.sidebar.write("Free Agent Machine")
# Selected Team Players
players = streamlit_return_players_on_team(team)
player_drop_down = ["Select a Player"] + players
player_to_drop = st.sidebar.selectbox(
     "Player to Drop", player_drop_down)
# Free Agents
free_agents = get_league_free_agents()
fa_drop_down = ["Select a Player"] + free_agents
player_to_add = st.sidebar.selectbox(
    "Player to Add", fa_drop_down)
# Compute Transaction
# if st.sidebar.button('Simulate Transaction') and player_to_drop in players and player_to_add in \
#         free_agents:
with st.spinner(f"Simulating transaction. Dropping {player_to_drop} and adding {player_to_add}..."):
    current_players_9cat_averages, current_team_9cat_averages, new_players_9cat_averages, \
        new_team_9cat_averages, difference_team_9cat_averages = streamlit_waiver_add_and_drop(
            team_9cat_stats, player_to_drop, player_to_add)
    # # st.write("Current Roster 9Cat Averages")
    # st.table(current_team_9cat_averages.style.format(STREAMLIT_TABLE_FORMAT))
    # # st.write("New Roster 9Cat Averages")
    # st.table(new_team_9cat_averages.style.format(STREAMLIT_TABLE_FORMAT))
    # # st.write("9Cat Averages Roster Differences")
    # st.table(difference_team_9cat_averages.style
    transaction_dataframe = combine_current_new_differnce_dataframes_player_transaction(
        current_team_9cat_averages, new_team_9cat_averages, difference_team_9cat_averages)
    try:
        transaction_dataframe.drop("TEAM", axis=1, inplace=True)
    except:
        pass
    st.table(transaction_dataframe.style.applymap(
        color_negative_red, subset=pd.IndexSlice["Difference",
            ["FG_PCT", "FT_PCT", "FG3M", "PTS", "REB", "AST", "STL", "BLK"]]).applymap(
        color_negative_red_tov, subset=pd.IndexSlice["Difference", ["TOV"]]).format(
        STREAMLIT_TABLE_FORMAT))




# Add line break
st.write("")
st.subheader("Team Power Rankings")
st.write("The Power Ranking feature will calculate the 9Cat averages of each team in the League. "
         "Use this tool to see how your team ranks against other League teams in each of "
         "the 9 categories. This process will take 10-15 minutes the first time you run it. "
         "On further attempts to run it, the information will be presented quickly.")
st.write("")
if st.button('Power Rankings'):
    # Compute league averages
    with st.spinner(f"Getting the entire league's team information. This may take a while..."):
        league_averages_dataframe = league_averages(league_team_list)
        league_averages_dataframe_index = clean_league_averages_dataframe(league_averages_dataframe)
        league_power_rankings = power_rankings(league_averages_dataframe)
        league_power_rankings_index = get_overall_power_rank(league_power_rankings)

        ranking_change_dataframe = get_average_and_power_ranking_change(
            league_averages_dataframe, team_dict, new_team_9cat_averages)
        ranking_change_dataframe = ranking_change_dataframe.iloc[:, :-1]

    st.table(league_averages_dataframe_index)
    st.write("The table below shows the leagues Power Rankings (PR). For each category, a team is "
             "ranked ")
    st.table(league_power_rankings_index)

    st.table(ranking_change_dataframe.style.applymap(color_power_rank, subset=pd.IndexSlice[:,  \
        ["FG_PCT", "FT_PCT", "FG3M", "PTS", "REB", "AST","STL", "BLK"]]).applymap(
        color_power_rank_tov, subset=pd.IndexSlice[:, ["TOV"]]))


team1 = st.selectbox(
     'Lebrontourage Teams',
     ("Select a Team", AUTOPICK[NAME_KEY], CRABBEHERBYTHEPUSSY[NAME_KEY],
      EL_LADRON_DE_CABRAS[NAME_KEY], LALALAND[NAME_KEY], MAGICS_JOHNSON[NAME_KEY],
      MCCURRY[NAME_KEY], NUNN_OF_YALL_BETTA[NAME_KEY], RUSTY_CUNTBROOKS[NAME_KEY],
      SWAGGY_P[NAME_KEY], TVONS_TIP_TOP_TEAM[NAME_KEY], WAKANDA_FOREVER[NAME_KEY],
      YOBITCH_TOPPIN_ME[NAME_KEY]), 0, key="team1")

LEAGUE_TEAM_NAMES = [AUTOPICK[NAME_KEY], CRABBEHERBYTHEPUSSY[NAME_KEY],
                     EL_LADRON_DE_CABRAS[NAME_KEY], LALALAND[NAME_KEY], MAGICS_JOHNSON[NAME_KEY],
                     MCCURRY[NAME_KEY], NUNN_OF_YALL_BETTA[NAME_KEY], RUSTY_CUNTBROOKS[NAME_KEY],
                     SWAGGY_P[NAME_KEY], TVONS_TIP_TOP_TEAM[NAME_KEY], WAKANDA_FOREVER[NAME_KEY],
                     YOBITCH_TOPPIN_ME[NAME_KEY]]


if team1 not in LEAGUE_TEAM_NAMES:
    st.warning('Select a team...')
    st.stop()

# Reference variables
if team1 == AUTOPICK[NAME_KEY]:
    team1_dict = AUTOPICK
elif team1 == CRABBEHERBYTHEPUSSY[NAME_KEY]:
    team1_dict = CRABBEHERBYTHEPUSSY
elif team1 == EL_LADRON_DE_CABRAS[NAME_KEY]:
    team1_dict = EL_LADRON_DE_CABRAS
elif team1 == LALALAND[NAME_KEY]:
    team1_dict = LALALAND
elif team1 == MAGICS_JOHNSON[NAME_KEY]:
    team1_dict = MAGICS_JOHNSON
elif team1 == MCCURRY[NAME_KEY]:
    team1_dict = MCCURRY
elif team1 == NUNN_OF_YALL_BETTA[NAME_KEY]:
    team1_dict = NUNN_OF_YALL_BETTA
elif team1 == RUSTY_CUNTBROOKS[NAME_KEY]:
    team1_dict = RUSTY_CUNTBROOKS
elif team1 == SWAGGY_P[NAME_KEY]:
    team1_dict = SWAGGY_P
elif team1 == TVONS_TIP_TOP_TEAM[NAME_KEY]:
    team1_dict = TVONS_TIP_TOP_TEAM
elif team1 == WAKANDA_FOREVER[NAME_KEY]:
    team1_dict = WAKANDA_FOREVER
elif team1 == YOBITCH_TOPPIN_ME[NAME_KEY]:
    team1_dict = YOBITCH_TOPPIN_ME

team2 = st.selectbox(
     'Lebrontourage Teams',
     ("Select a Team", AUTOPICK[NAME_KEY], CRABBEHERBYTHEPUSSY[NAME_KEY],
      EL_LADRON_DE_CABRAS[NAME_KEY], LALALAND[NAME_KEY], MAGICS_JOHNSON[NAME_KEY],
      MCCURRY[NAME_KEY], NUNN_OF_YALL_BETTA[NAME_KEY], RUSTY_CUNTBROOKS[NAME_KEY],
      SWAGGY_P[NAME_KEY], TVONS_TIP_TOP_TEAM[NAME_KEY], WAKANDA_FOREVER[NAME_KEY],
      YOBITCH_TOPPIN_ME[NAME_KEY]), 0, key="team2")

LEAGUE_TEAM_NAMES = [AUTOPICK[NAME_KEY], CRABBEHERBYTHEPUSSY[NAME_KEY],
                     EL_LADRON_DE_CABRAS[NAME_KEY], LALALAND[NAME_KEY], MAGICS_JOHNSON[NAME_KEY],
                     MCCURRY[NAME_KEY], NUNN_OF_YALL_BETTA[NAME_KEY], RUSTY_CUNTBROOKS[NAME_KEY],
                     SWAGGY_P[NAME_KEY], TVONS_TIP_TOP_TEAM[NAME_KEY], WAKANDA_FOREVER[NAME_KEY],
                     YOBITCH_TOPPIN_ME[NAME_KEY]]


if team2 not in LEAGUE_TEAM_NAMES:
    st.warning('Select a team...')
    st.stop()

# Reference variables
if team2 == AUTOPICK[NAME_KEY]:
    team2_dict = AUTOPICK
elif team2 == CRABBEHERBYTHEPUSSY[NAME_KEY]:
    team2_dict = CRABBEHERBYTHEPUSSY
elif team2 == EL_LADRON_DE_CABRAS[NAME_KEY]:
    team2_dict = EL_LADRON_DE_CABRAS
elif team2 == LALALAND[NAME_KEY]:
    team2_dict = LALALAND
elif team2 == MAGICS_JOHNSON[NAME_KEY]:
    team2_dict = MAGICS_JOHNSON
elif team2 == MCCURRY[NAME_KEY]:
    team2_dict = MCCURRY
elif team2 == NUNN_OF_YALL_BETTA[NAME_KEY]:
    team2_dict = NUNN_OF_YALL_BETTA
elif team2 == RUSTY_CUNTBROOKS[NAME_KEY]:
    team2_dict = RUSTY_CUNTBROOKS
elif team2 == SWAGGY_P[NAME_KEY]:
    team2_dict = SWAGGY_P
elif team2 == TVONS_TIP_TOP_TEAM[NAME_KEY]:
    team2_dict = TVONS_TIP_TOP_TEAM
elif team2 == WAKANDA_FOREVER[NAME_KEY]:
    team2_dict = WAKANDA_FOREVER
elif team2 == YOBITCH_TOPPIN_ME[NAME_KEY]:
    team2_dict = YOBITCH_TOPPIN_ME


total_difference_dataframe, total_difference_dataframe_colored = weekly_matchup_evaluator(
    team1_dict, team2_dict, team1_9cat_average_stats_data=team_9cat_stats,
                             team2_9cat_average_stats_data=None, week="current", season=2020)

st.table(total_difference_dataframe_colored)


