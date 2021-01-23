import requests
from bs4 import BeautifulSoup
import json
import datetime as dt

class NBA_Spreads:
    def __init__(self):
        self.path = '/home/pi/NBA-led-Scoreboard/NBASpreads.json'
        
    def New_Day(self):
        url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/basketball/nba'

        response = requests.get(url).json()
        data = {}
        for game in response[0]['events']:
            
            if game['type'] != 'GAMEEVENT' or game['live'] == True:
                #print('Not a game.')
                continue
            
            gamelink = game['link'][0:len(game['link'])-4]
            if dt.datetime.strftime(dt.datetime.now(), '%Y%m%d') != gamelink[len(gamelink)-8:len(gamelink)]:
                #print(gamelink[len(gamelink)-9:-1])
                continue
            data[gamelink] = {}
            data[gamelink]['hometeam'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['description']
            data[gamelink]['awayteam'] = game['displayGroups'][0]['markets'][1]['outcomes'][0]['description']
            data[gamelink]['spread'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['price']['handicap']
            data[gamelink]['over_under'] = game['displayGroups'][0]['markets'][2]['outcomes'][0]['price']['handicap']
            
        with open(self.path, 'w') as file:
            json.dump(data, file)
            
        return None
            
    def Spreads_Update(self):
        url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/basketball/nba'

        response = requests.get(url).json()
        
        with open(self.path, 'r') as file:
            data = json.load(file)
            
        for game in response[0]['events']:
            
            if game['type'] != 'GAMEEVENT' or game['live'] == True:
                continue
            
            gamelink = game['link'][0:len(game['link'])-4]
            if dt.datetime.strftime(dt.datetime.now(), '%Y%m%d') != gamelink[len(gamelink)-8:len(gamelink)]:
                continue
            data[gamelink] = {}
            data[gamelink]['hometeam'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['description']
            data[gamelink]['awayteam'] = game['displayGroups'][0]['markets'][1]['outcomes'][0]['description']
            data[gamelink]['spread'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['price']['handicap']
            data[gamelink]['over_under'] = game['displayGroups'][0]['markets'][2]['outcomes'][0]['price']['handicap']
        
        with open(self.path, 'w') as file:
            json.dump(data, file)
            
        return None

if __name__ == '__main__':
    #NBA_Spreads().Spreads_Update()
    NBA_Spreads().New_Day()