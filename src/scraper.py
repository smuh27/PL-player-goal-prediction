import requests, re
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from io import StringIO


all_player_path = '../data/processed/player_shooting_2023_2024.csv'

# URLs of players' pages
haaland_url = 'https://fbref.com/en/players/1f44ac21/Erling-Haaland'
# similar_players_url = {
#     'Dovbyk': 'https://fbref.com/en/players/5b847bb0/Artem-Dovbyk', 
#     'Kane': 'https://fbref.com/en/players/21a66f6a/Harry-Kane', 
#     'Osimhen': 'https://fbref.com/en/players/8c90fd7a/Victor-Osimhen', 
#     'Joselu': 'https://fbref.com/en/players/6265208f/Joselu', 
#     'Vlahovic': 'https://fbref.com/en/players/79443529/Dusan-Vlahovic'
# }


def clean_data(file_path, drop_columns=[]):
    df = pd.read_csv(file_path)
    df.drop(columns=drop_columns, inplace=True)
    return df



def get_table_by_name(soup, table_name):
    tables = soup.find_all('table')
    for table in tables:
        caption = table.find('caption')
        if caption and table_name.lower() in caption.text.lower():
            return pd.read_html(StringIO(str(table)), header=1)[0]
    return None

def get_player_name(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    name_span = soup.find('h1').find('span')
    return name_span.text.strip() if name_span else None

def get_last_5_seasons_by_age(data_list, current_age):
    data_list['Age'] = pd.to_numeric(data_list['Age'], errors='coerce').fillna(0).astype(int)
    last_5_seasons_data = data_list[(data_list['Age'] <= current_age) & (data_list['Age'] > current_age - 5)]
    return last_5_seasons_data

def scrape_player_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    player = get_player_name(url)
    print(f"Fetching data for: {player}")
    
    shoot_stats = get_table_by_name(soup, 'Shooting')
    standard_stats = get_table_by_name(soup, 'Standard Stats')

    if shoot_stats is None or standard_stats is None:
        raise ValueError("Required tables not found on the page")

    current_age = standard_stats['Age'].dropna().apply(pd.to_numeric, errors='coerce').fillna(0).astype(int).max()
    
    last5_shoot = get_last_5_seasons_by_age(shoot_stats, current_age)
    last5_standard = get_last_5_seasons_by_age(standard_stats, current_age)
    
    shooting_columns_to_keep = ['Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt']
    standard_columns_to_keep = ['Season', 'Age', 'Squad', 'Country', 'Comp', '90s', 'LgRank', 'MP', 'Starts', 'Min', 'Gls', 'xG', 'npxG', 'xAG']

    shooting_list = last5_shoot[shooting_columns_to_keep].copy()
    standard_list = last5_standard[standard_columns_to_keep].copy()

    standard_list['Gls'] = pd.to_numeric(standard_list['Gls'], errors='coerce')
    standard_list['90s'] = pd.to_numeric(standard_list['90s'], errors='coerce')
    standard_list['Gls/90'] = standard_list['Gls'] / standard_list['90s']

    data_list = pd.concat([standard_list, shooting_list], axis=1)
    return data_list

if __name__ == "__main__":
    data = scrape_player_data(haaland_url)
    # for player_name, player_url in similar_players_url.items():
    #     similar_data = scrape_player_data(player_url)
    #     similar_data.to_csv(f'../data/processed/{player_name}_stats.csv', index=False)
    # all_player_data = clean_data(all_player_path,['Unnamed'])
    # all_player_data.to_csv('../data/processed/player_shooting_2023_2024.csv', index=False)
    data.to_csv('../data/processed/Haaland_stats.csv', index=False)
    print("Data scraped and saved.")
    