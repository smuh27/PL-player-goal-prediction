import requests, re
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from io import StringIO


haaland_url = 'https://fbref.com/en/players/1f44ac21/Erling-Haaland'
similar_players_url = {'Dovbyk' : 'https://fbref.com/en/players/5b847bb0/Artem-Dovbyk', 'Kane' : 'https://fbref.com/en/players/21a66f6a/Harry-Kane', 'Osimhen': 'https://fbref.com/en/players/8c90fd7a/Victor-Osimhen', 'Joselu' : 'https://fbref.com/en/players/6265208f/Joselu', 'Vlahovic': 'https://fbref.com/en/players/79443529/Dusan-Vlahovic' }

def scrape_player_data(url):
    response = requests.get(url).text
    response_io = StringIO(response)


    shoot_stats = pd.read_html(response_io, header=1)[4]
    standard_stats = pd.read_html(response_io, header=1)[3]


    last5_shoot = shoot_stats.iloc[3:9].reset_index(drop=True)
    last5_standard = standard_stats.iloc[3:9].reset_index(drop=True)
    shooting_columns_to_keep = ['Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT']
    standard_columns_to_keep = ['Season', 'Age', 'Squad', 'Country', 'Comp', '90s', 'LgRank', 'MP', 'Starts', 'Min', 'Gls', 'xG']


    shooting_list = last5_shoot[shooting_columns_to_keep].copy()
    standard_list = last5_standard[standard_columns_to_keep].copy()


    standard_list.loc[:, 'Gls'] = pd.to_numeric(standard_list['Gls'], errors='coerce')
    standard_list.loc[:, '90s'] = pd.to_numeric(standard_list['90s'], errors='coerce')


    standard_list['Gls/90'] = standard_list['Gls'] / standard_list['90s']

    addition_shooting_stats = last5_shoot['Dist']

    data_list = pd.concat([standard_list, shooting_list, addition_shooting_stats], axis=1)

    return data_list

    
    




if __name__ == "__main__":
    data = scrape_player_data(haaland_url)
    for player_name, player_url in similar_players_url.items():
        similar_data = scrape_player_data(player_url)
        similar_data.to_csv(f'../data/processed/{player_name}_stats.csv', index=False)
    
    data.to_csv('../data/processed/Haaland_stats.csv', index=False)
    print("Data scraped and saved to 'data/processed_data.csv'.")
