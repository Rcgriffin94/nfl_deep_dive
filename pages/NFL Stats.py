import streamlit as st
from functions import get_all_games
import nfl_stats_plotly

st.header("NFL Stats")
st.set_page_config(page_title='NFL Stats', layout='wide')

all_games = get_all_games()

col1, col2 = st.columns(2)
with col1:
    filter_toggle = st.radio(label='Do you want to filter by date?', options=['Yes', 'No'])
with col2:
    if filter_toggle == 'Yes':
        date_range = st.date_input('Select a date range', value=[])
        try:
            date_range_start, date_range_end = date_range
        except (NameError, ValueError):
            st.warning('Please select a date range')
            st.stop()
    elif filter_toggle == 'No':
        date_range_start = all_games['gameday'].min()
        date_range_end = all_games['gameday'].max()

st.divider()

all_games = all_games[(all_games['gameday'] >= date_range_start) & (all_games['gameday'] <= date_range_end)]
if all_games.empty == True:
    st.warning('No NFL games in this timeframe')
    st.stop()
    
st.header(f'Analyzing {len(all_games):,} games since {date_range_start.strftime('%m/%d/%Y')}')

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(nfl_stats_plotly.team_winning_pct(all_games))
with col4:
    st.plotly_chart(nfl_stats_plotly.qb_winning_pct(all_games))
col5, col6 = st.columns(2)    
with col5:
    st.plotly_chart(nfl_stats_plotly.avg_points_per_game(all_games))
with col6:
    st.write('Placeholder')

with st.expander(label="View raw data"):
    st.dataframe(all_games)

