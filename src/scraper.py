import requests, re
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from io import StringIO

# def has_same_characters(string1, string2):
#     # Count the frequency of characters in both strings
#     freq1 = {}
#     freq2 = {}
#     for char in string1:
#         freq1[char] = freq1.get(char, 0) + 1
#     for char in string2:
#         freq2[char] = freq2.get(char, 0) + 1
    
#     # Check if the frequencies of characters are the same in both strings
#     return freq1 == freq2


# url = 'https://www.bbc.com/sport/football/premier-league/top-scorers'
# data = requests.get(url).text
# soup = BeautifulSoup(data, 'html.parser')


# tables = soup.find_all('table')
# table = soup.find('table', class_='gs-o-table')
# pattern = re.compile(r'^(.*?)\b(?:([A-Z][a-z]*)\b|$)')
# # 'Goals', 'Played', 'GPM', 'MPG', 'Total Shots', 'Goal Conversion', 'Shot Accuracy'
# data_list = []
# for row in table.tbody.find_all('tr'):
#     columns = row.find_all('td')
#     if (columns != []):
#         # Find the player name and team name elements
#         player_name_element = row.find('div', class_='sp-c-top-scorers__player-name')
#         team_name_element = row.find('div', class_='sp-c-top-scorers__teams')
#         # Extract text content from the elements
#         goal = columns[2].text.strip()
#         played = columns[4].text.strip()
#         gpm = columns[5].text.strip()
#         mpg = columns[6].text.strip()
#         total_shots = columns[7].text.strip()
#         goal_conv = columns[8].text.strip()
#         shot_acc = columns[9].text.strip()

#         player_name = player_name_element.text.strip()
#         team_name = team_name_element.text.strip()
#         names = player_name.split()
#         last_name = names[1::2]
#         data_list.append({'FirstName': ''.join(names[::2]), 'LastName': ''.join(last_name), 'Goals': goal, 'Played': played, 'GPM': gpm, 'MPG': mpg, 'Total Shots': total_shots, 'Goal Conversion': goal_conv, 'Shot Accuracy': shot_acc})




# for i in range(len(data_list)):
#     string2 = data_list[i]['LastName']
#     string1 = data_list[i]['FirstName']
#     if (has_same_characters(string1, string2) == True):
#         string2 = ''
#     string2 = string2[len(string2)//2:]
#     data_list[i]['LastName'] = string2
#     df = pd.DataFrame(data_list)
haaland_url = 'https://fbref.com/en/players/1f44ac21/Erling-Haaland'


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


    data_list = pd.concat([standard_list, shooting_list], axis=1)

    return data_list

def scrape_similar_player_data():
    response = requests.get(url).text
    response_io = StringIO(response)
    


if __name__ == "__main__":
    data = scrape_player_data(haaland_url)
    data.to_csv('../data/processed/haaland_stats.csv', index=False)
    print("Data scraped and saved to 'data/processed_data.csv'.")