import pandas as pd
import functions
import plotly.express as px

def winning_pct(df):

    games_played = df['home_team'].value_counts() + df['away_team'].value_counts()
    wins = df['winner'].value_counts()
    winning_pct = (wins / games_played * 100).round(2)

    team_stats = pd.DataFrame({
        'Total Games': games_played,
        'Wins': wins,
        'Winning Pct': winning_pct
    }).fillna(0)

    fig = px.bar(data_frame=team_stats,
             x=team_stats.index,
             y='Winning Pct',
             title='Team Winning Percentage')
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    fig.update_xaxes(tickangle=90)

    return fig

