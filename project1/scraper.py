import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sqlalchemy import create_engine

url = 'https://www.scrapethissite.com/pages/forms/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

teams_list = []

def scrap_page(link):
  page = requests.get(urljoin(url, link))
  page_soup = BeautifulSoup(page.content, 'html.parser')
  table = page_soup.select("table.table tr.team")
  for team in table:
    team = {
      "name": team.select_one("td.name").get_text(),
      "year": team.select_one("td.year").get_text(),
      "wins": team.select_one("td.wins").get_text(),
      "losses": team.select_one("td.losses").get_text(),
      "winning_percent": team.select_one("td.pct").get_text(),
      "goals_for": team.select_one("td.gf").get_text(),
      "goals_against": team.select_one("td.ga").get_text()
    }
    teams_list.append(team)

pages = soup.select("ul.pagination li")[:-1]
for page in pages:
  page_link = page.find('a').get("href")
  scrap_page(link=page_link)



#---------------TRANSFORMATION-----------------
df = pd.DataFrame(teams_list)
cols_to_fix = ['year', 'wins', 'losses', 'winning_percent', 'goals_for', 'goals_against']
for col in cols_to_fix:
  df[col] = pd.to_numeric(df[col], errors='coerce')

df['goal_diff'] = df['goals_for'] - df['goals_against']

#---- LOADING (PostgreSQL) ----
pg_user = "root"
pg_pass = "root"
pg_host = "localhost"
pg_port = "5432"
pg_db = "nhl_stats"
url = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
engine = create_engine(url)

df.head(0).to_sql(
  name='match_stats',
  con=engine,
  if_exists='replace'
)
df.to_sql(
  name="match_stats",
  con=engine,
  if_exists='append'
)

