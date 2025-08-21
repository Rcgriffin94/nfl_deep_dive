import pandas as pd
import datetime as dt
import numpy as np

def get_all_games():

    all_games = pd.read_csv('https://raw.githubusercontent.com/nflverse/nfldata/refs/heads/master/data/games.csv')
    cols_to_keep = ['away_coach', 'away_qb_id', 'away_qb_name',
        'away_score', 'away_team', 'div_game', 'game_id', 'game_type', 'gameday', 'gametime',
        'home_coach', 'home_qb_id', 'home_qb_name', 'home_score', 'home_team', 'location',
        'nfl_detail_id', 'overtime', 'referee', 'roof', 'season', 'stadium',
        'stadium_id', 'surface', 'temp', 'total','week', 'weekday', 'wind']

    all_games = all_games[cols_to_keep]

    all_games['winner'] = np.where(all_games['home_score'] > all_games['away_score'], all_games['home_team'],
                            np.where(all_games['away_score'] > all_games['home_score'], all_games['away_team'], 'Tie'))
    
    all_games['winning_qb'] = np.where(all_games['winner'] == all_games['home_team'], all_games['home_qb_name'], all_games['away_qb_name'])

    all_games['gameday'] = pd.to_datetime(all_games['gameday']).dt.date
    all_games = all_games[all_games['gameday'] <= dt.date.today()]
    all_games.sort_values(['gameday', 'gametime'], ascending=False, inplace=True)
    all_games.reset_index(drop=True, inplace=True)

    return all_games

def get_games_by_team(team_name):

    all_games = get_all_games()
    team_games = all_games[(all_games['away_team'] == team_name) | (all_games['home_team'] == team_name)]
    team_games.sort_values(['gameday', 'gametime'], ascending=False, inplace=True)
    team_games.reset_index(drop=True, inplace=True)

    return team_games
