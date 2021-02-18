import requests
from NBA_File_Handler import *
import time
import datetime as dt
from NBA_Spreads import *

class NBA_Data:
    
    
    def __init__(self):
        self.game_data = requests.get('https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json').json()['scoreboard']['games']
        print(str(dt.datetime.strftime(dt.datetime.now(), '%m/%d/%Y %H:%M')) + ' - NBA Data Gathered')
    
    def JSON_dump(self):
        NBA_FILE_HANDLER().JSON_GAMEDATA(self.game_data, 'DataToday')
        #with open('/home/pi/Documents/NBAlog.txt', 'a') as file:
        live = False
        later_today = False
        for game in self.game_data:
            if game['gameStatus'] == 3: #game Finished
                continue
            if game['gameStatus'] == 2: #game is live
                live = True
            if game['gameStatus'] == 1: #game later today
                if later_today == False and game['gameStatusText'] != 'PPD': #if this passes,  then this is the next game
                    next_game = game['gameTimeUTC']
                    later_today = True
            
        if live == False and later_today == True: #No games rn but there will be later today
            wait_time = (dt.datetime.strptime(next_game, '%Y-%m-%dT%H:%M:%SZ') - dt.datetime.utcnow()).total_seconds()
            string = 'Next game in ' + '{:4.1f}'.format(wait_time/3600) + ' hours.\n'
            print(str(dt.datetime.strftime(dt.datetime.now(), '%m/%d/%Y %H:%M')) + ' - ' + string)
            with open('/home/pi/Documents/NBAlog.txt', 'a') as file:
                file.write(string)
            #print('Write success')
            try:
                #print('Sleeping for ' + str(wait_time + 120) + ' seconds.')
                time.sleep(wait_time + 120)
            except ValueError:
                print(str(dt.datetime.strftime(dt.datetime.now(), '%m/%d/%Y %H:%M')) + ' - Game is about to start')
                
        if live == False and later_today == False: #No more games today, wait until the API updates for the next day
            string = ' - No more games today.'
            print(str(dt.datetime.strftime(dt.datetime.now(), '%m/%d/%Y %H:%M')) + string)
            #with open('/home/pi/Documents/NBAlog.txt', 'a') as file:
            #    file.write(string)
            time.sleep(3600*2)
            print("")
            #sleep for 2 hours
        if live == True:
            NBA_Spreads().Spreads_Update()
            print(str(dt.datetime.strftime(dt.datetime.now(), '%m/%d/%Y %H:%M')) + ' - Live game.')
        
if __name__ == '__main__':
    test = True
    while test == True:
        #try:
        NBA_Data().JSON_dump()
        #print('Successfully gathered data.')
        #except:
        #print('Error requesting data - retrying in 120 seconds')
        time.sleep(120)
        #test = False
