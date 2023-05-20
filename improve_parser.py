import requests
from bs4 import BeautifulSoup
import json

time_url = requests.get("https://mosff.ru/team/11").text #получение инфы о команде
page = BeautifulSoup(time_url, "lxml") #получение супа
 
links_all = page.find_all("a", class_="composition__link composition__link--color text-light") #получение ссылок на всех игроков команды
list_of_links = [] # лист всех ссылок на страницы игроков
for k in links_all: # заполнение массива
    a = k.get("href")
    list_of_links.append( "https://mosff.ru" + a )

team_info = {} # общий словарь, где ключ имя футболиста, а значение - это другой словарь

for link in list_of_links:
    player_info = {}
    page = requests.get(link).text 
    soup = BeautifulSoup(page, "lxml")
    name = soup.find("a", class_="profile__title").text # получение имени игрока
    player_info["Имя"] = name
    property_info = soup.find_all("div", class_="profile__property")
    property_value = soup.find_all("div", class_="profile__value")
    for i in range(len(property_info)):
        player_info[property_info[i].text.strip()] = property_value[i].text.strip()\
    
    stats = soup.find_all("table", class_="table table-statistics table--dominant-color") #поиск всех стат игрока
    stat_garbage = [] # МАССИВ, КУДА БУДУ СКЛАДЫВАТЬ
    stat = [] # Финальные статы
    for t in stats: # заполнение массива
        stat_garbage.append(t.text.strip().replace("\n", " ").split("  "))
    
    for k in stat_garbage:
        for j in k:
            if j == "":
                pass
            else:
                stat.append(j)
    main_stat = stat[0:5]
    goals = stat[5:18]
    discipline = stat[18:-1]
    player_info[main_stat[0]] = main_stat[1:]
    player_info[goals[0]] = goals[1:]
    player_info[discipline[0]] = discipline[1:]
    with open(f"players_info/{name}.json", "w") as file:
        json.dump(player_info, file, indent=4, ensure_ascii=False)
