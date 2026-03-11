import sqlite3
import pandas as pd

conn = sqlite3.connect('./db/baseball-stats_20_23.db')

hitting = pd.read_csv('./csv/hitting_leaders.csv')
pitching = pd.read_csv('./csv/pitching_leaders.csv')
standing = pd.read_csv('./csv/team_standings.csv')





hitting.to_sql('hitting', conn, if_exists='replace', index=False)
pitching.to_sql('pitching', conn, if_exists='replace', index=False)
standing.to_sql('standing', conn, if_exists='replace', index=False)


conn.close()