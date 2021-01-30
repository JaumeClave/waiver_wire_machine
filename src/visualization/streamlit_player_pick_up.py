import pandas as pd
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from src.data import player_9cat_average as p9ca
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import commonplayerinfo
import streamlit as st


NBA = "nba"
SEASON = 2020
JSON_FOLDER = r"C:\Users\Jaume\Documents\Python Projects\waiver_wire_machine\references\oauth2.json"
NAME_KEY = "name"
GAMES_COLUMN = "GAMES"
MEAN_ROW = "mean"
TEAM_KEY = "team_key"
PLAYER_COLUMN = "PLAYER"
TEAM_COLUMN = "TEAM"
EDITORIAL_TEAM_FULL_NAME = "editorial_team_full_name"
UNIFORM_NUMBER = "uniform_number"
COMMON_ALL_PLAYERS ="CommonAllPlayers"
PERSON_ID_KEY = "PERSON_ID"
TEAM_CITY_KEY = "TEAM_CITY"
TEAM_NAME_KEY = "TEAM_NAME"
COMMON_PLAYER_INFO = "CommonPlayerInfo"
JERSEY_KEY = "JERSEY"
DISPLAY_FIRST_LAST = "DISPLAY_FIRST_LAST"
RANK_SUFFIX ="_RANK"
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

THREE_DECIMAL_COLUMNS = [FIELD_GOAL_PERCENTAGE_COLUMN, FREE_THROW_PERCENTAGE_COLUMN]
ONE_DECIMAL_COLUMNS = [THREES_MADE_COLUMN, POINTS_COLUMN, REBOUNDS_COLUMN, ASSITS_COLUMN,
                       STEALS_COLUMN, BLOCKS_COLUMN, TURNOVERS_COLUMN]

STREAMLIT_TABLE_FORMAT = {"FG_PCT" : p9ca.THREE_DECIMAL_FORMAT,
                          "FT_PCT" : p9ca.THREE_DECIMAL_FORMAT, "FG3M" : p9ca.TWO_DECIMAL_FORMAT,
                          "PTS" : p9ca.TWO_DECIMAL_FORMAT, "REB" : p9ca.TWO_DECIMAL_FORMAT,
                          "AST" : p9ca.TWO_DECIMAL_FORMAT, "STL" : p9ca.TWO_DECIMAL_FORMAT,
                          "BLK" : p9ca.TWO_DECIMAL_FORMAT, "TOV" : p9ca.TWO_DECIMAL_FORMAT}

# Team dictionaries
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


def yahoo_fantasy_api_authentication():

    sc = OAuth2(None, None, from_file=JSON_FOLDER)

    return sc


def yahoo_fantasy_league(sc):

    gm = yfa.Game(sc, NBA)
    league_id_list = gm.league_ids(year=SEASON)
    league_id = "".join(str(id) for id in league_id_list)
    league = gm.to_league(league_id)

    return league


def yahoo_player_team_and_jersey(player_name):

    player_details_dictionary = league.player_details(player_name)
    players_team = player_details_dictionary[0][EDITORIAL_TEAM_FULL_NAME]
    players_number = player_details_dictionary[0][UNIFORM_NUMBER]

    return players_team, players_number


def player_ids_by_nba_team_name(nba_team):

    common_all_players = commonallplayers.CommonAllPlayers(is_only_current_season=1)
    common_all_players_dict = common_all_players.get_normalized_dict()[COMMON_ALL_PLAYERS]
    player_ids_in_team_list = [player[PERSON_ID_KEY] for player in common_all_players_dict if \
        player[TEAM_CITY_KEY] + " " + player[TEAM_NAME_KEY] == nba_team]

    return player_ids_in_team_list


def nba_player_name_from_jersey_search(team_player_ids, yahoo_jersey_number):

    for id in team_player_ids:
        nba_jersey_number = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict() \
            [COMMON_PLAYER_INFO][0][JERSEY_KEY]
        if nba_jersey_number == yahoo_jersey_number:
            nba_name = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict() \
            [COMMON_PLAYER_INFO][0][DISPLAY_FIRST_LAST]

            return nba_name


def yahoo_name_to_nba_name(yahoo_player_name):
    """ Function expectes a Yahoo player name and it will find the players Team Name and Jersey
    Number. It then searches the NBA API for Player IDs belonging to found Team Name. For every
    Player ID it searches their Jersey Number. When there is a match, it returns the NBA Player
    Name.
    """

    player_team, player_number = yahoo_player_team_and_jersey(yahoo_player_name)
    player_ids_in_team_list = player_ids_by_nba_team_name(player_team)
    nba_player_name = nba_player_name_from_jersey_search(player_ids_in_team_list, player_number)

    return nba_player_name


def create_roster_dataframe(player_list):

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

    team = league.to_team(team_dictionary[TEAM_KEY])
    team_roster = team.roster()
    player_in_team_list = [player[NAME_KEY] for player in team_roster]

    roster_dataframe = create_roster_dataframe(player_in_team_list)

    roster_dataframe = format_roster_dataframe(roster_dataframe)

    return roster_dataframe


def fantasy_team_mean_stats(roster_dataframe, team_dictionary):

    mean_series = roster_dataframe.loc[MEAN_ROW]
    mean_series[PLAYER_COLUMN] = team_dictionary[NAME_KEY]
    team_mean_dataframe = pd.DataFrame(mean_series).T
    team_mean_dataframe = team_mean_dataframe.rename(columns={PLAYER_COLUMN : TEAM_COLUMN})
    team_mean_dataframe.reset_index(inplace=True, drop=True)

    return team_mean_dataframe


def player_to_team_mean_stats(team_dictionary, league):
    """
    This function creates a dataframe containing the season averaged stats for each player on a
    Fantasy Team. It then finds the average stats for the entire team and returns a single row
    dataframe with the Fantasy Team name and its seasoned averaged 9cat stats.
    """

    roster_dataframe = team_9cat_average_stats(team_dictionary, league)
    team_mean_dataframe = fantasy_team_mean_stats(roster_dataframe, team_dictionary)

    return team_mean_dataframe


@st.cache(show_spinner=False)
def league_averages(league_team_list):

    league_averages_dataframe = pd.DataFrame()
    for team in league_team_list:
        sc = yahoo_fantasy_api_authentication()
        league = yahoo_fantasy_league(sc)
        league_averages_dataframe = league_averages_dataframe.append(player_to_team_mean_stats
                                                                     (team, league))
    league_averages_dataframe.reset_index(drop=True, inplace=True)
    return league_averages_dataframe


def yahoo_player_team_and_jersey(player_name):

    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    player_details_dictionary = league.player_details(player_name)
    players_team = player_details_dictionary[0][EDITORIAL_TEAM_FULL_NAME]
    players_number = player_details_dictionary[0][UNIFORM_NUMBER]

    return players_team, players_number


def player_ids_by_nba_team_name(nba_team):

    common_all_players = commonallplayers.CommonAllPlayers(is_only_current_season=1)
    common_all_players_dict = common_all_players.get_normalized_dict()[COMMON_ALL_PLAYERS]
    player_ids_in_team_list = [player[PERSON_ID_KEY] for player in common_all_players_dict if \
        player[TEAM_CITY_KEY] + " " + player[TEAM_NAME_KEY] == nba_team]

    return player_ids_in_team_list


def nba_player_name_from_jersey_search(team_player_ids, yahoo_jersey_number):

    for id in team_player_ids:
        nba_jersey_number = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict() \
            [COMMON_PLAYER_INFO][0][JERSEY_KEY]
        if nba_jersey_number == yahoo_jersey_number:
            nba_name = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict() \
            [COMMON_PLAYER_INFO][0][DISPLAY_FIRST_LAST]

            return nba_name


def yahoo_name_to_nba_name(yahoo_player_name):
    """ Function expectes a Yahoo player name and it will find the players Team Name and Jersey
    Number. It then searches the NBA API for Player IDs belonging to found Team Name. For every
    Player ID it searches their Jersey Number. When there is a match, it returns the NBA Player
    Name.
    """

    player_team, player_number = yahoo_player_team_and_jersey(yahoo_player_name)
    player_ids_in_team_list = player_ids_by_nba_team_name(player_team)
    nba_player_name = nba_player_name_from_jersey_search(player_ids_in_team_list, player_number)

    return nba_player_name


# Function to return team dataframe with 9cat averages
def remove_mean_and_player(team_players_9cat_stats_dataframe, player_to_drop):

    team_players_9cat_stats_dataframe = team_players_9cat_stats_dataframe.drop(MEAN_ROW)
    team_players_9cat_stats_dataframe = \
        team_players_9cat_stats_dataframe[~team_players_9cat_stats_dataframe[PLAYER_COLUMN]
    .str.contains(player_to_drop)]

    return team_players_9cat_stats_dataframe

@st.cache(show_spinner=False)
def waiver_add_and_drop(fantasy_team, player_to_drop, player_to_add):

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

    for column in dataframe.columns:
        dataframe[column] = dataframe[column].astype(float)

    return dataframe


def drop_add_mean_9cat_difference(current_9cat, new_9cat):

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

    current_players_9cat_averages, current_team_9cat_averages, new_players_9cat_averages, \
    new_team_9cat_averages = waiver_add_and_drop(team, player_to_drop, player_to_add)

    difference_team_9cat_averages = drop_add_mean_9cat_difference(current_team_9cat_averages,
                                                  new_team_9cat_averages)

    visualise_team_9cat_averages(player_to_drop, player_to_add, current_team_9cat_averages,
                             new_team_9cat_averages, difference_team_9cat_averages, visualise)

    return current_players_9cat_averages, current_team_9cat_averages, new_players_9cat_averages, \
           new_team_9cat_averages, difference_team_9cat_averages


def new_league_9cat_averages(league_average_dataframe, team, new_team_9cat_averages):

    removed_team_dataframe = league_average_dataframe[~league_average_dataframe[TEAM_COLUMN].str\
        .contains(team[NAME_KEY])]

    new_team_9cat_averages[TEAM_COLUMN] = team[NAME_KEY]
    added_team_dataframe = removed_team_dataframe.append(new_team_9cat_averages)
    added_team_dataframe.reset_index(drop=True, inplace=True)

    return added_team_dataframe


def team_dataframe_column_float(roster_dataframe):

    for column in roster_dataframe.columns[1:]:
        roster_dataframe[column] = roster_dataframe[column].astype(float)

    return roster_dataframe


def change_in_power_rankings(league_averages_dataframe, team, player_to_drop, player_to_add):

    current_players_9cat_averages, current_team_9cat_averages, new_players_9cat_averages, \
    new_team_9cat_averages = compare_team_9cats_on_transaction(team, player_to_drop,
                                                           player_to_add, visualise=False)

    # New league average dataframe
    new_league_averages_dataframe = new_league_9cat_averages(league_averages_dataframe,
                                                          team, new_team_9cat_averages)

    new_league_averages_dataframe = team_dataframe_column_float(new_league_averages_dataframe)

    # Get new rankings
    new_league_power_rankings = power_rankings(new_league_averages_dataframe).sort_values(TEAM_COLUMN)
    # Get current rankings
    current_league_power_rankings = power_rankings(league_averages_dataframe).sort_values(TEAM_COLUMN)

    # Drop Team column
    new_league_power_rankings = new_league_power_rankings.reset_index(drop=True)
    new_league_power_rankings = new_league_power_rankings.drop(TEAM_COLUMN, axis=1)
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

    return power_rankings_difference


def power_ranking_change(league_averages_dataframe, team, new_team_9cat_averages):

    # New league average dataframe
    new_league_averages_dataframe = new_league_9cat_averages(league_averages_dataframe,
                                                          team, new_team_9cat_averages)

    new_league_averages_dataframe = team_dataframe_column_float(new_league_averages_dataframe)

    # Get new rankings
    new_league_power_rankings = power_rankings(new_league_averages_dataframe).sort_values(TEAM_COLUMN)
    # Get current rankings
    current_league_power_rankings = power_rankings(league_averages_dataframe).sort_values(TEAM_COLUMN)

    # Drop Team column
    new_league_power_rankings = new_league_power_rankings.reset_index(drop=True)
    new_league_power_rankings = new_league_power_rankings.drop(TEAM_COLUMN, axis=1)
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

    return power_rankings_difference


# Function power ranking
def power_rankings(dataframe):

    power_ranking_dataframe =  dataframe.copy()
    try:
        power_ranking_dataframe.drop(MEAN_ROW, inplace=True)
    except KeyError:
        pass
    for column in power_ranking_dataframe.columns[1:]:

        sorted_points = power_ranking_dataframe[column].sort_values(ascending=False)
        sorted_points.drop_duplicates(inplace=True)

        sorting_dictionary = dict()

        count = 1
        for point in sorted_points:
            sorting_dictionary[point] = count
            count += 1

        power_ranking_dataframe[column + RANK_SUFFIX] = power_ranking_dataframe[column].map\
            (sorting_dictionary)

    power_ranking_dataframe.drop(dataframe.columns[1:], axis=1, inplace=True)

    return power_ranking_dataframe


def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = '#EC7063' if val < 0 else '#52BE80'
    return 'color: %s' % color


def get_team_id_from_team_name(team_name):

    return "".join([x[TEAM_KEY] for x in league_team_list if x[NAME_KEY] == team_name])


def team_player_list(team_id):
    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    team = league.to_team(team_id)
    team_roster = team.roster()
    player_in_team_list = [player[NAME_KEY] for player in team_roster]

    return player_in_team_list


def streamlit_return_players_on_team(team_name):

    team_id = get_team_id_from_team_name(team_name)
    player_list = team_player_list(team_id)

    return player_list

@st.cache(show_spinner=False)
def get_league_free_agents():
    # Free agents
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
def get_team_roster(team_dict):
    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
    team_9cat_stats = team_9cat_average_stats(team_dict, league)

    return team_9cat_stats

@st.cache(show_spinner=False, allow_output_mutation=True)
def streamlit_waiver_add_and_drop(current_9cat_roster_averages, player_to_drop, player_to_add):

    sc = yahoo_fantasy_api_authentication()
    league = yahoo_fantasy_league(sc)
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


# Streamlit Code
st.title('Free Agent Machine')
st.subheader("Use this tool to discover how a player add/drop transaction impacts your teams 9cat stats.")
st.write("Firstly, select your team. Secondly, select the player you want to drop. Thirdly, "
         "select the FA you want to add. Compare!")
st.write("")

# Sidebar select Team, Player to Drop and Player to Add
team = st.sidebar.selectbox(
     'Lebrontourage Teams',
     (AUTOPICK[NAME_KEY], CRABBEHERBYTHEPUSSY[NAME_KEY], EL_LADRON_DE_CABRAS[NAME_KEY],
      LALALAND[NAME_KEY], MAGICS_JOHNSON[NAME_KEY], MCCURRY[NAME_KEY],
      NUNN_OF_YALL_BETTA[NAME_KEY], RUSTY_CUNTBROOKS[NAME_KEY], SWAGGY_P[NAME_KEY],
      TVONS_TIP_TOP_TEAM[NAME_KEY], WAKANDA_FOREVER[NAME_KEY], YOBITCH_TOPPIN_ME[NAME_KEY]))

# Reference variables
if team == AUTOPICK[NAME_KEY]:
    team_dict = AUTOPICK
elif team == CRABBEHERBYTHEPUSSY[NAME_KEY]:
    team_dict = CRABBEHERBYTHEPUSSY
elif team == EL_LADRON_DE_CABRAS[NAME_KEY]:
    team_dict = EL_LADRON_DE_CABRAS
elif team == LALALAND[NAME_KEY]:
    team_dict = LALALAND
elif team == MAGICS_JOHNSON[NAME_KEY]:
    team_dict = MAGICS_JOHNSON
elif team == MCCURRY[NAME_KEY]:
    team_dict = MCCURRY
elif team == NUNN_OF_YALL_BETTA[NAME_KEY]:
    team_dict = NUNN_OF_YALL_BETTA
elif team == RUSTY_CUNTBROOKS[NAME_KEY]:
    team_dict = RUSTY_CUNTBROOKS
elif team == SWAGGY_P[NAME_KEY]:
    team_dict = SWAGGY_P
elif team == TVONS_TIP_TOP_TEAM[NAME_KEY]:
    team_dict = TVONS_TIP_TOP_TEAM
elif team == WAKANDA_FOREVER[NAME_KEY]:
    team_dict = WAKANDA_FOREVER
elif team == YOBITCH_TOPPIN_ME[NAME_KEY]:
    team_dict = YOBITCH_TOPPIN_ME

# Load team dataframe
with st.spinner(f"Getting {team} Team Information..."):
    team_9cat_stats = get_team_roster(team_dict)

# Selected Team Players
players = streamlit_return_players_on_team(team)
player_to_drop = st.sidebar.selectbox(
     "Player to Drop", players)

# Free Agents
free_agents = get_league_free_agents()
player_to_add = st.sidebar.selectbox("Player to Add", free_agents)

# Compute Transaction
# if st.sidebar.button('Compare!'):
with st.spinner(f"Simulating transaction. Dropping {player_to_drop} and adding {player_to_add}..."):
    current_players_9cat_averages, current_team_9cat_averages, new_players_9cat_averages, \
        new_team_9cat_averages, difference_team_9cat_averages = streamlit_waiver_add_and_drop(
        team_9cat_stats, player_to_drop, player_to_add)

st.write("Current Roster 9Cat Averages")
st.table(current_team_9cat_averages.style.format(STREAMLIT_TABLE_FORMAT))

st.write("New Roster 9Cat Averages")
st.table(new_team_9cat_averages.style.format(STREAMLIT_TABLE_FORMAT))

st.write("9Cat Averages Roster Differences")
st.table(difference_team_9cat_averages.style.applymap(color_negative_red).\
         format(STREAMLIT_TABLE_FORMAT))

# Add line break
st.write("")
st.write("The Power Ranking feature will calculate the 9Cat averages of each team in the League. "
         "This process will take 10-15 minutes the first time you run it. On further attempts to "
         "run it, the information will be presented instantly.")
if st.button('Power Rankings'):
    # Compute league averages
    with st.spinner(f"Getting the Entire League's Team Information..."):
        league_averages_dataframe = league_averages(league_team_list)
    ranking_chnage = power_ranking_change(league_averages_dataframe, team_dict, new_team_9cat_averages)
    st.table(ranking_chnage)



