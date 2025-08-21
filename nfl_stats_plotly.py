import pandas as pd
import functions
import plotly.express as px

def team_winning_pct(df):

    home_team_games = df[['home_team', 'winner']].copy()
    home_team_games["team"] = home_team_games["home_team"]
    home_team_games["is_winner"] = home_team_games["team"] == home_team_games["winner"]

    away_team_games = df[["away_team", "winner"]].copy()
    away_team_games["team"] = away_team_games["away_team"]
    away_team_games["is_winner"] = away_team_games["team"] == away_team_games["winner"]

    all_games = pd.concat([home_team_games[["team", "is_winner"]], away_team_games[["team", "is_winner"]]])

    team_stats = (
        all_games.groupby("team")
        .agg(
            games_played=("is_winner", "count"),
            wins=("is_winner", "sum")
        )
    )

    team_stats["win_pct"] = team_stats["wins"] / team_stats["games_played"]

    team_stats = team_stats.reset_index()
    team_stats = team_stats.sort_values("win_pct", ascending=False)

    fig = px.bar(
        team_stats,
        x="win_pct",
        y="team",
        orientation="h",
        text="win_pct",
        hover_data=["wins", "games_played"],
        title="Winning Percentage by Team"
    )

    fig.update_layout(
            xaxis={'categoryorder': 'total descending'}, 
            xaxis_tickformat=".2%",
            xaxis_title = 'Winning Percentage',
            yaxis_title = 'Team Name',
        )
    fig.update_traces(texttemplate="%{text:.2%}", hovertemplate="Team: %{y}<br>Win %: %{x:.2%}<br>Wins: %{customdata[0]}<br>Games: %{customdata[1]}")
    fig.update_xaxes(tickangle=60)

    return fig

def qb_winning_pct(df):
    qb_wins = df['winning_qb'].value_counts()
    qb_wins = qb_wins.reset_index()
    qb_wins.columns = ["quarterback_name", "win_count"]

    fig = px.bar(
        qb_wins.head(25),  # top 10
        x="quarterback_name",
        y="win_count",
        title="Top 25 most winningest quarterbacks",
        text="win_count"
    )

    fig.update_layout(
        xaxis={'categoryorder': 'total descending'},
        xaxis_title='Quarterback Name',
        yaxis_title='Win Count'
    )
    fig.update_xaxes(tickangle=60)

    return fig

def avg_points_per_game(df):
    home = df[['home_team', 'home_score', 'away_score']].copy()
    home.rename(columns={
        "home_team": "team",
        "home_score": "points_scored",
        "away_score": "points_allowed"
        }, inplace=True
    )

    away = df[["away_team", "away_score", "home_score"]].copy()
    away.rename(columns={
        "away_team": "team",
        "away_score": "points_scored",
        "home_score": "points_allowed"
    }, inplace=True)

    team_points = pd.concat([home, away])
    team_points = team_points.groupby('team').sum(['points_scored', 'points_allowed'])
    team_points = team_points.reset_index()
    team_points['points_differential'] = team_points['points_scored'] - team_points['points_allowed']
    team_points = team_points.sort_values("team")

    fig = px.bar(
        data_frame=team_points,
        x='team',
        y='points_differential',
        title='Point differential by team',
        text='points_differential'
    )

    fig.update_layout(
        xaxis_title='Team Name',
        yaxis_title='Point differential'
    )


    return fig