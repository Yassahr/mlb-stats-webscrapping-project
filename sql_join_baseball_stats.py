import sqlite3
import pandas as pd


def table_hitting_standing_join():
    with sqlite3.connect("./db/baseball-stats_20_23.db") as conn:
        query="""
        SELECT Statistics, 
            Name,
            [Stat Number],
            Region,
            Wins,
            Loses,
            Ties,
            WP,
            Standing,
            h.Team,
            h.Year
        FROM standing as s
        JOIN hitting AS h 
        ON h.Year = s.Year
        AND h.Team = s.Team
        AND h.League = s.League
        """

        try:
            df = pd.read_sql_query(query, conn)
            df.info()
            print(df.head(10))
            return df
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            # conn.close()
            print('Tables Joined')
table_hitting_standing_join()

def table_pitching_standing_join():
    with sqlite3.connect("./db/baseball-stats_20_23.db") as conn:
        query="""
            SELECT Statistics, 
                Name,
                [Stat Number],
                p.Team,
                p.Year
            FROM standing as s
            JOIN pitching AS p 
            ON p.Year = s.Year
            AND p.Team = s.Team
            """
        try:
            df = pd.read_sql_query(query, conn)
            df.info()
            print(df.head(10))
            return df

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            # conn.close()
            print('Tables Joined')
table_pitching_standing_join()


