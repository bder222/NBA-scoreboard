import requests
import json

team_ids = {1: 'ATL', 2: 'BOS', 3: 'NO', 4: 'CHI', 5: 'CLE', 6: 'DAL', 7: 'DEN', 8: 'DET', 9: 'GS', 10: 'HOU', 11: 'IND', 12: 'LAC', 13: 'LAL', 14: 'MIA', 15: 'MIL', 16: 'MIN', 17: 'BKN', 18: 'NY', 19: 'ORL', 20: 'PHI', 21: 'PHX', 22: 'POR', 23: 'SAC', 24: 'SA', 25: 'OKC', 26: 'UTAH', 27: 'WSH', 28: 'TOR', 29: 'MEM', 30: 'CHA'}



class NBA_Standings:
    def __init__ (self):
        self.path = '/home/pi/NBA-scoreboard/NBAStandings.json'
    
    def Standings(self):
        standings = {'eastern':{}, 'western':{}}
        for conference in [5,6]:
            
            response = requests.get("https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2022/types/2/groups/{0}/standings/0".format(conference)).json()
            if conference == 5:
                conf = 'eastern'
            elif conference == 6:
                conf = 'western'

            for team_id in response['standings']:
                team = team_ids[int(team_id['team']['$ref'][84:team_id['team']['$ref'].find('?')])]
                if team == 'NY':
                    team = 'NYK'
                elif team == 'WSH':
                    team = 'WAS'
                elif team == 'UTAH':
                    team = 'UTA'
                elif team == 'GS':
                    team = 'GSW'
                elif team == 'SA':
                    team = 'SAS'
                elif team == 'NO':
                    team = 'NOP'
                standings[conf][team] = {
                    'seed': int(team_id['records'][0]['stats'][0]['value']),
                    'wins': int(team_id['records'][0]['stats'][1]['value']),
                    'losses': int(team_id['records'][0]['stats'][2]['value']),
                    }
                
            with open(self.path, 'w') as file:
                json.dump(standings, file)
        return standings

if __name__ == '__main__':
    stack = NBA_Standings().Standings()