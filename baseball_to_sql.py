import sqlite3
import pandas as pd
import os

def create_database():
    if not os.path.exists('./db/baseball-stats_20_23.db'):
        try:
                conn = sqlite3.connect('./db/baseball-stats_20_23.db')

                hitting = pd.read_csv('./csv/hitting_leaders.csv')
                pitching = pd.read_csv('./csv/pitching_leaders.csv')
                standing = pd.read_csv('./csv/team_standings.csv')



                hitting.to_sql('hitting', conn, if_exists='replace', index=False)
                pitching.to_sql('pitching', conn, if_exists='replace', index=False)
                standing.to_sql('standing', conn, if_exists='replace', index=False)

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            print('Database created')
    else:
        print('Database already exists')
create_database()