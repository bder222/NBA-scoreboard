import requests
from bs4 import BeautifulSoup
import json
import datetime as dt

class NBA_Spreads:
    def __init__(self):
        self.path = '/home/pi/NBA-scoreboard/NBASpreads.json'
        self.path_live = '/home/pi/NBA-scoreboard/NBASpreadsLive.json'
        
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
            try:
                data[gamelink] = {}
                data[gamelink]['hometeam'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['description']
                data[gamelink]['awayteam'] = game['displayGroups'][0]['markets'][1]['outcomes'][0]['description']
                data[gamelink]['spread'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['price']['handicap']
                data[gamelink]['over_under'] = game['displayGroups'][0]['markets'][2]['outcomes'][0]['price']['handicap']
            except: 
                print("Error gathering spread data")
        with open(self.path, 'w') as file:
            json.dump(data, file)
        
        
        return None
            
    def Spreads_Update(self):
        url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/basketball/nba'

        response = requests.get(url).json()
        
        with open(self.path, 'r') as file:
            data = json.load(file)
        
        with open(self.path_live, 'r') as file:
            data_live = json.load(file)
            
        for game in response[0]['events']:
            
            if game['type'] != 'GAMEEVENT' or game['live'] == True:
                continue
            
            gamelink = game['link'][0:len(game['link'])-4]
            if dt.datetime.strftime(dt.datetime.now(), '%Y%m%d') != gamelink[len(gamelink)-8:len(gamelink)]:
                continue
            try:
                data[gamelink] = {}
                data[gamelink]['hometeam'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['description']
                data[gamelink]['awayteam'] = game['displayGroups'][0]['markets'][1]['outcomes'][0]['description']
                data[gamelink]['spread'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['price']['handicap']
                data[gamelink]['over_under'] = game['displayGroups'][0]['markets'][2]['outcomes'][0]['price']['handicap']
            except:
                print("Error gathering spread data")
        
        with open(self.path, 'w') as file:
            json.dump(data, file)
        
        data_live = {}
        for game in response[0]['events']:
            
            if game['type'] != 'GAMEEVENT' or game['live'] != True:
                #print('Not a game.')
                continue
            
            gamelink = game['link'][0:len(game['link'])-4]
            if dt.datetime.strftime(dt.datetime.now(), '%Y%m%d') != gamelink[len(gamelink)-8:len(gamelink)]:
                #print(gamelink[len(gamelink)-9:-1])
                continue
            try:
                data_live[gamelink] = {}
                data_live[gamelink]['hometeam'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['description']
                data_live[gamelink]['awayteam'] = game['displayGroups'][0]['markets'][1]['outcomes'][0]['description']
                data_live[gamelink]['spread'] = game['displayGroups'][0]['markets'][1]['outcomes'][1]['price']['handicap']
                data_live[gamelink]['over_under'] = game['displayGroups'][0]['markets'][2]['outcomes'][0]['price']['handicap']
            except:
                print('Error gatehring live data')
        with open(self.path_live, 'w') as file:
            json.dump(data_live, file)
        
        return None

if __name__ == '__main__':
    #NBA_Spreads().Spreads_Update()
    NBA_Spreads().New_Day()
    
    
#Set up a script similar to the NBA data that updates spreads every 2 minutes for live data only
#Sync spreads update and new day to both start at noon, offset the updates by one minute
