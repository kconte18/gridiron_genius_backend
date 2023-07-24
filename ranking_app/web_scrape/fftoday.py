import requests
import pandas as pd
from bs4 import BeautifulSoup

urls=['https://www.fftoday.com/rankings/playerrank.php?o=4&RankType=redraft&Scoring=1&LeagueID=1', 'https://www.fftoday.com/rankings/playerrank.php?o=4&RankType=redraft&Scoring=3&LeagueID=1']

def web_scrape():
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        s_list = soup.find_all('td', class_='smallbody', align='LEFT')
        s_list = s_list[0:100]
        player_list = []
        rank_list = []
        rank_num = 1
        for s in s_list:
            player_list.append(s.text.strip())
            rank_list.append(rank_num)
            rank_num = rank_num + 1

        ranking_data = {'player_name':player_list, 'rank':rank_list}
        df = pd.DataFrame(ranking_data)
        print(df)