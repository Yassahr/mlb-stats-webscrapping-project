from io import StringIO
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


LEAGUES = {
    'a': range(2020, 2023), 
    'n': range(2020, 2023),
}

wait_time = 1         


hitting_stats="csv/hitting_leaders.csv"
pictching_stats="csv/pitching_leaders.csv"
standing_states="csv/team_standings.csv"



def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

count=0

def table_to_df(table_element, year, league):
    html = table_element.get_attribute("outerHTML")
    df = pd.read_html(StringIO(html))[0]

    df = df.dropna(how="all")
    df = df[~df[0].str.contains("American League|A.L. History|A.L.,Team|National League", na=False)]

    df["year"]   = year
    df["league"] = league

    return df


def baseball_scrape():
    driver = create_driver()

    hitting_df = pd.DataFrame()
    pitching_df = pd.DataFrame()
    standings_df = pd.DataFrame()

    total_pages = sum(len(list(yrs)) for yrs in LEAGUES.values())
    scraped = 0

    for league_code, years in LEAGUES.items():
        league_name = "AL" if league_code == "a" else "NL"

        for year in years:
            url = f"https://www.baseball-almanac.com/yearly/yr{year}{league_code}.shtml"
            scraped += 1
            print(f"[{scraped}/{total_pages}] Scraping {league_name} {year} -- {url}")

            try:
                driver.get(url)
                time.sleep(wait_time)
                tables = driver.find_elements(By.CSS_SELECTOR, "table.boxed")

                if not tables:
                    print(f" No table element found")
                    continue

                if len(tables) >= 1:
                    hitting_df = pd.concat([hitting_df, table_to_df(tables[0], year, league_name)], ignore_index=True)
                else:
                    print(f"Hitting table not found")

                if len(tables) >= 2:
                    pitching_df = pd.concat([pitching_df, table_to_df(tables[1], year, league_name)], ignore_index=True)
                else:
                    print("Pitching table not found")

                if len(tables) >= 3:
                    standings_df = pd.concat([standings_df, table_to_df(tables[2], year, league_name)], ignore_index=True)
                else:
                    print("Standings table not found")

            except Exception as e:
                print(f"  Error scraping {league_name} {year}: {e}")
                continue

#data cleaning the hitting data
    #renaming the columns
    hitting_df.columns= ["Statistics", "Name",  "Team", "Stat Number", "Top", "Year", "League"]
    #dropping dup header rows
    hitting_df = hitting_df.drop_duplicates(subset=["Statistics","Name","Team","Stat Number","Top"])
    hitting_df=hitting_df.loc[1:]
    #removing sematically functionless column
    hitting_df=hitting_df.drop(columns=['Top'])
    hitting_df["Stat Number"]= hitting_df["Stat Number"].astype('float')
    print(hitting_df.head(10))
    hitting_df.info()
    hitting_df.to_csv(hitting_stats, mode="a", header=True, index=False)


#data cleaning pitch data
    #renaming the columns
    pitching_df.columns= ["Statistics", "Name",  "Team", "Stat Number", "Top", "Year", "League"]
    #dropping dup header rows
    pitching_df = pitching_df.drop_duplicates(subset=["Statistics","Name","Team","Stat Number","Top"])
    #removing sematically functionless column
    pitching_df=pitching_df.drop(columns=['Top'])
    pitching_df=pitching_df.loc[1:]
    pitching_df["Stat Number"]= pitching_df["Stat Number"].astype('float')
    pitching_df.to_csv(pictching_stats, mode="a", header=True, index=False)


#data cleaning for standing  
    #adding column names
    standings_df.columns= ["Region", "Team",  "Wins", "Loses", "Ties", "WP", "Standing", "Year", "League"]
    standings_df = standings_df[~standings_df['Team'].str.contains("Roster", na=False)]
    #replacing -- with 0
    standings_df= standings_df.replace('--', 0)
    standings_df= standings_df.replace('-', 0)

    #Confirming each imput is the correct type
    standings_df['Region']=standings_df['Region'].astype('str')
    standings_df['Team']= standings_df['Team'].astype('str')
    standings_df['Wins']=standings_df['Wins'].astype('int')
    standings_df['Loses']=standings_df['Loses'].astype('int')
    standings_df['Ties']=standings_df['Ties'].astype('int')
    standings_df['WP']=standings_df['WP'].astype('float')
    standings_df['Year']=standings_df['Year'].astype('int')
    standings_df['League']=standings_df['League'].astype('str')
    standings_df.to_csv(standing_states, mode="a", header=True, index=False)

    driver.quit()
    print('Files loaded to CSV')


if __name__ == "__main__":
    baseball_scrape()