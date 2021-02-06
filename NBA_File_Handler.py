import json
import os
import datetime as dt

class NBA_FILE_HANDLER:
    
    
    
    def __init__(self):
        self.path = '/home/pi/NBA-scoreboard/'
        
    def JSON_GAMEDATA(self, gamedata, date):
        
        try:
            #print(os.system('who'))
            with open(self.path + '{0}.json'.format(date), 'w') as file:
                json.dump(gamedata, file)
                #os.system('chmod 777 ' + self.path + '{0}.json'.format(date))
        except FileNotFoundError:
            os.makedirs(self.path + str(date))
            with open(self.path + '{0}.json'.format(date), 'w') as file:
                json.dump(gamedata, file)
    def CLEAR_WEEK(self):
        for file in os.listdir(self.path):
            if file != '.DS_Store':
                os.unlink(self.path + file)
    def CLEAR_YESTERDAY(self):
        yesterday = dt.datetime.now() - dt.timedelta(days=1)
        for file in os.listdir(self.path):
            if file == (yesterday.strftime('%m.%d.%y') + '.json'):
                os.unlink(self.path + file)
    def CLEAR_TODAY(self):
        yesterday = dt.datetime.now() - dt.timedelta(days=0)
        for file in os.listdir(self.path):
            if file == (yesterday.strftime('%m.%d.%y') + '.json'):
                os.unlink(self.path + file)
        
        
data = [[{'HomeTeam': 'CHE', 'AwayTeam': 'TOT', 'HomeScore': '2', 'AwayScore': '1', 'Status': 'Full Time', 'GameDate': '02.22.20'}, {'HomeTeam': 'SOU', 'AwayTeam': 'AVL', 'HomeScore': '2', 'AwayScore': '0', 'Status': 'Full Time', 'GameDate': '02.22.20'}, {'HomeTeam': 'CRY', 'AwayTeam': 'NEW', 'HomeScore': '1', 'AwayScore': '0', 'Status': 'Full Time', 'GameDate': '02.22.20'}, {'HomeTeam': 'SHU', 'AwayTeam': 'BHA', 'HomeScore': '1', 'AwayScore': '1', 'Status': 'Full Time', 'GameDate': '02.22.20'}, {'HomeTeam': 'BUR', 'AwayTeam': 'BOU', 'HomeScore': '3', 'AwayScore': '0', 'Status': 'Full Time', 'GameDate': '02.22.20'}, {'HomeTeam': 'LEI', 'AwayTeam': 'MCI', 'HomeScore': '0', 'AwayScore': '1', 'Status': 'Full Time', 'GameDate': '02.22.20'}], [], []]
data2 = [{'hello': 0}]
if __name__ == '__main__':
    instance = EPL_FILE_HANDLER()
    instance.JSON_GAMEDATA(data, '07.15.20')
    
