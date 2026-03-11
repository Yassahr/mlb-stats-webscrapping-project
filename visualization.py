import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from sql_join_baseball_stats import *

hitting_stats=table_hitting_standing_join()
pitching_stats=table_pitching_standing_join()
st.title("2020-2023 Baseball Statistical Breakdown Based on Team and Player")

#Figure 1
#Pitching Grouped By Stat + Normalized for values of different magnitude
pitching_grouped_by_year=pitching_stats.groupby(['Year','Name','Statistics'])['Stat Number'].sum().reset_index()
print(pitching_grouped_by_year.columns)
#Dropdown
all_years = sorted(set(pitching_grouped_by_year['Year'].unique()) | set(hitting_stats['Year'].unique()))
year = st.selectbox('Select Year', all_years)

pitching_grouped_by_year['Total'] = pitching_grouped_by_year.groupby(['Year','Statistics'])['Stat Number'].transform('sum')
pitching_grouped_by_year['Percentage'] = (pitching_grouped_by_year['Stat Number'] / pitching_grouped_by_year['Total']) * 100

year_filter = pitching_grouped_by_year[pitching_grouped_by_year['Year'] == year]

#This chart shows each statistics and which Players dominate the stats in each catergory
fig = px.bar(
    year_filter,
    x='Statistics',
    y='Percentage',
    color='Name',
    text=year_filter['Stat Number'],
    title=f'{year} Pitching Stats By Player',
    labels={'Percentage': '% Percent', 'Statistics': 'Statistics'},
)

fig.update_layout(
    barmode='stack',
)

st.plotly_chart(fig)




#Figure 2
#Dropdown Function
hitting_stat_by_year = hitting_stats[hitting_stats['Year'] == year].copy()
#Inverting WP since lower number means more wins
hitting_stat_by_year['WP'] = 1 - hitting_stat_by_year['WP']
#Shows insights for the relationship between the stats and the team winning percentage
fig2 = px.bar(
    hitting_stat_by_year,
    x='Name',
    y='WP',
    color='Team',
    hover_data=['Name', 'Statistics'],
    labels={'Stat Number': 'Player Stat Value', 'WP': 'Team Win %'},
    title=f'Player Stat Number vs Team Win Percentage ({year})',
)
fig2.update_layout(
    barmode='stack',
)
st.plotly_chart(fig2, use_container_width=True)



#Graph 3 shows winning percentage vs the amount of wins each team has
fig3, ax1 = plt.subplots(figsize=(20, 10))
team_wins = hitting_stat_by_year.groupby("Team")["Wins"].mean().sort_values(ascending=False)
#inverted WP
team_wp = 1-hitting_stat_by_year.groupby("Team")["WP"].mean().reindex(team_wins.index)
#Subplot 1 winning bar graph
ax1.bar(team_wins.index, 
        team_wins.values, 
        color="#008080",
)
ax1.set_xlabel("Team", fontsize=30)
ax1.set_ylabel("Wins", color="#008080", fontsize=30)
#Graph 2 winning WP graph
ax2 = ax1.twinx()
ax1.tick_params(axis='both', labelsize=20)
ax2.tick_params(axis='both', labelsize=20)
ax2.plot(team_wins.index, team_wp.values, color="#9E4200", marker="o")
ax2.set_ylabel("Win Percentage", color="#9E4200", fontsize=30 )
ax1.set_title(f"Wins vs Win Percentage by Team — {year}", fontsize=50)
ax1.set_xticklabels(team_wins.index, rotation=45, ha="right", fontsize=13)
st.pyplot(fig3, use_container_width=True)